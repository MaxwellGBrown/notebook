.. _sqlalchemy_objects_between_sessions:

===============================
Moving Objects Between Sessions
===============================

Sometimes you have two different sessions, and an object that you want to move
between them with its ORM data in tact.

There's a few things to consider:

#. After committing an object or before accessing it, all of it's values are
   **expired** meaning that their values aren't pulled from the database yet.
#. Objects outside of a session cannot update their values, and are considered
   "detached".

Using ``make_transient``, objects can keep their values while detached,
allowing them to either be manipulated w/o the session & database, or to be
added to a different session.

SQLAlchemy's `state management <http://docs.sqlalchemy.org/en/latest/orm/session_state_management.html>`__ doc page has an in-depth overview of object states.

make_transient
--------------

.. code-block:: python

    from sqlalchemy.orm.session import make_transient, make_transient_to_detached

    Session1.commit()  # unrelated to transient-ing; expires all objects within

    # remove object from session
    Session1.refresh(obj)  # re-up all expired attributes
    make_transeint(obj)  # remove object from session but save attr values

    # add object to session
    make_transient_to_detached(obj)  # fully detaches obj, expires all attrs
    Session.add(obj)  # adds object back to session based on pk


``make_transient`` and ``make_transient_to_detached`` are "wizard" functions
provided to manage ORM objects between sessions.

``make_transient`` takes all the currently loaded values of the ORM object and
and freezes them, while setting all un-loaded objects to ``None``. This allows
one to use the ORM object like a typical object.

``make_transient_to_detached`` takes an ORM object in the detached state (e.g.
a transient object) and detaches it, allowing the object to be re-attached to a
session. 




