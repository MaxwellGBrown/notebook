=======================================
Transient ORM Object Test Data Fixtures
=======================================

When operating tests that interact with a database, having test data to base
the tests on is important.

However, the database sessions you're setting up your fixtures with won't
necessarily be the same session you're testing against.

Yet, you might still want the ORM objects created by the fixture that represent
the test data.

By changing the ORM's object state to *transient* or *detached* it can be
referenced without being a part of a session (see `SQLAlchemy's State
Management docs <http://docs.sqlalchemy.org/en/latest/orm/session_state_management.html>`__).

.. note:: 

    **Transient or Detached?**

    Frankly... I'm not 100% sure. Based off the docs, Detached sounds more like
    what this example is trying to accomplish (an object whose data is
    available, but is not attached to a session).

    However, in practice I had a decent amount of issues working with the
    Detached objects while the Transient objects worked as intended.

    This example is based on a test suite built into a tightly-coupled
    application.

    Added to the confusion are the significant changes between object states
    between sqlalchemy v1.0 and v1.1.

    There are bound to be some mistakes in this example, but it should provide
    a decent starting point for implementing the next iteration of pytest ORM
    fixtures.


Test Data from a Fixture
------------------------

In the below example, we're using the ORM class ``Foo`` to create test data
associate with that object and return it in a *transient* state. 

.. code-block:: python

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.session import make_transient, make_transient_to_detached

    from models.app.foo import Foo  # ORM class

    @pytest.fixture()
    def test_foo(request, config, alembic_head):

        # connect to database
        engine = create_engine(config['database'])
        session = sessionmaker(bind=engine)()

        # create test object using ORM classes
        foo = Foo(bar="Hello World")

        # commit the test object to the database
        session.add(foo)
        session.commit()

        # set up the OBJECT so it's not detached as Session opens & closes
        session.refresh(foo)  # reload all values from DB
        make_transient(foo)  # change foo's state to transient
        # make_transient_to_detached(foo)  # change to detached

        # close connection
        session.remove()

        def remove_test_foo():
            session = sessionmaker(bind=engine)()
            Foo.query.delete()  # delete all Foo objects
            session.commit()

        request.addfinalizer(remove_test_foo)

        return foo  # return transient (or detached) ORM object

.. note::

  Be mindful of this test-objects scope. If this object has a lot of
  dependencies it might be better off at a higher level scope. But in that same
  facet, if the object is added to a tests' session it will no longer be
  transient after that test concludes!

  `SQLAlchemy1.1's state-change events
  <http://docs.sqlalchemy.org/en/latest/orm/session_state_management.html#session-referencing-behavior>`__
  might provide a solution to this; if event handlers can be attached to
  specific fixtures it *may* provide a solution.


The Benefits
------------

The benefits of having the same ORM object that your tests may be manipulating
to reference against are **huge**!

A transient/detached object can be used to reference expected values without
running a query

.. code-block:: python

    def test_bar_in_index(test_foo, test_app):
        response = test_app.get("/")
        assert "Foo.bar = " + test_foo.bar in response


A detached/transient object provides all the info you might need to re-query a
non-transient object.

.. code-block:: python

    def test_change_bar(test_foo, test_app):
        response = test_app.post(
                "/edit/{}".format(test_foo.foo_id),
                params={"bar": "Hello Goodbye!"}
                )

        # query same id as test_foo
        changed_foo = Foo.query.filter_by(foo_id=test_foo.foo_id).one()
        assert changed_foo.bar == "Hello Goodbye!"

Alternatively the detached/transient object can be re-attached to a session to
be referenced without running a bunch of queryes (careful! make sure this
doesn't interfere with other tests scope-wise)

.. code-block:: python

    def test_change_bar(test_foo, test_app):
        response = test_app.post(
                "/edit/{}".format(test_foo.foo_id),
                params={"bar": "Hello Goodbye!"}
                )

        # session.add(test_foo)  # re-add if detached, unnecessary if transient
        session.refresh(test_foo)

        assert test_foo.bar == "Hello Goodbye!"
