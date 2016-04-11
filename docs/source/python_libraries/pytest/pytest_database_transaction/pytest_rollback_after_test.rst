.. _pytest_rollback_after_test:

===============================
Rollback transaction after test
===============================

Often in testing a program or application the test may rely on the application making changes to a database. However, that often means that the database state between tests in the same fixture, or that each test is relying on the previous test passing.

To alleviate this issue, a pytest fixture that handles a sqlalchemy *Engine-level Transaction* can rollback any low-level changes between tests.

This example borrows heavily from `Joining a Session into an External Transaction (such as for test suites) <http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites>`__ from the sqlalchemy docs.


Creating a Rollback Test Fixture
--------------------------------

First off, start by creating a pytest fixture that handles the creation of an engine-level transaction.

To do this, the ``engine`` and the ``Session`` (sesionmaker) must be readily available to the fixture.

.. code-block:: python

    import pytest

    @pytest.fixture(scope="function")
    def rollback(request):
        connection = engine.connect()
        transaction = connection.begin()
        session = Session(bind=connection)

        def revert_changes():
            session.close()
            transaction.rollback()
            connection.close()

        request.addfinalizer(revert_changes)
        return session

As far as the author can tell, this should handle separate transactions & connections. So, for instance, if one is testing an application that handles it's own separate connection to the engine, this *should* still roll back any changes made within the transaction.


Rolling Back Test Cases w/ Rollbacks
++++++++++++++++++++++++++++++++++++

Just like mentioned in the link to sqlalchemy's example (find the link above), if the test case needs rollback that requires a little bit of a different set up.

.. note::

   I (the author) have not had to do this yet, but it seemed like an easily translatable example. So hopefully this works!


.. code-block:: python
   :emphasize-lines: 2, 11, 14-18

    import pytest
    from sqlalchemy import event

    @pytest.fixture(scope="function")
    def rollback(request):
        connection = engine.connect()
        transaction = connection.begin()
        session = Session(bind=connection)

        # start a SAVEPOINT
        session.begin_nested()

        # then each time that SAVEPOINT ends, reopen it
        @event.listens_for(session, "after_transaction_end")
        def restart_savepoint(session, transaction):
            if transaction.nested and not transaction._parent.nested:
                session.expire_all()  # expire state just like session.commit()
                session.begin_nested()

        def revert_changes():
            session.close()
            transaction.rollback()
            connection.close()

        request.addfinalizer(revert_changes)
        return session


Rolling Back scoped_session Test Cases
--------------------------------------

Some applications leverage sqlalchemys concept of ``scoped_session`` which are used so that a single global session can be used to safely represent transactional sessions in a single thread.

This just requires a little bit of finagling to fit into our running example:

.. code-block:: python
   :emphasize-lines: 7, 10

    import pytest

    @pytest.fixture(scope="function")
    def rollback(request):
        connection = engine.connect()
        transaction = connection.begin()
        Session.configure(bind=connection)

        def revert_changes():
            Session.remove()
            transaction.rollback()
            connection.close()

        request.addfinalizer(revert_changes)
        return Session

.. note::

   Because ``scoped_session`` is one object that represents thread-safe sessions, using ``Session.configure(bind=connection)`` causes anything (like an application) that is calling ``Session`` to operate within the scope of that connection's transaction.

   Even if the application never interacts with the returned ``Session`` object, they're all representing the same thing and they'll all be bound to the same transaction.


Maintaining a Test Data Fixture w/ Transaction Rollbacks
--------------------------------------------------------

So, now that the concept of rolling back an engine-level transaction per test case has been established, it's possible to introduce a "parent fixture" that incorperates test data.

.. note::

  This example references the concepts of:

    * :ref:`nested fixtures <pytest_nested_fixtures>`
    * :ref:`alembic <alembic>`

The scope of a "test data" fixture should be introduced *at least* a scope level higher than the rollback fixture (since the rollback fixture is supposed to garuntee that the test data can be used in the same state between all test cases). 

Below is a real-life example of what creating test data might look like for a web application that leverages alembic & pytest. Note that there are some variables and modules that are redacted from this example because they're project/application specific.

.. code-block:: python

    import pytest

    import alembic
    from alembic.config import Config


    @pytest.fixture(scope="class")
    def alembic_head(request):
        class AlembicArgs(object):
            x = ['yaml_config=' + os.path.join(core.APP1_ROOT, "test.yaml")]

        alembic_cfg = Config(os.path.join(core.APP1_ROOT, 'alembic.ini'),
                cmd_opts=AlembicArgs)

        alembic.command.upgrade(alembic_cfg, "head")

        def alembic_base():
            alembic.command.downgrade(alembic_cfg, "base")

        request.addfinalizer(alembic_base)


    @pytest.fixture(scope="class")  # must be same or lower than alembic_head
    def test_data(request, alembic_head):
    """ Create test data for alembic's `head` version """
    app_model.connect(**connection_kwargs, poolclass=NullPool)

    # ADD TEST DATA

    app_model.Session.commit()  # scoped_session
    app_model.disconnect()  # scoped_session.remove() & connection.disconnect()

    def remove_test_data():
        app_model.connect(**connection_kwargs, poolclass=NullPool)

        # DELETE TEST DATA

        app_model.Session.commit()  # scoped_session
        app_model.disconnect()  # .remove() & .disconnect()

    request.addfinalizer(remove_test_data)

    @pytest.fixture(scope="function")
    def connection_rollback(request):
        engine = create_engine(**connection_kwargs, poolclass=None)
        connection = engine.connect()
        Base.metadata.bind = connection
        transaction = connection.begin()

        def revert_changes():
            Session.remove()
            transaction.rollback()
            connection.close()

        request.addfinalizer(revert_changes)
