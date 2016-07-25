==========
sqlalchemy
==========

sqlalchemy is a database management package that does anything you could ever imagine. Use it to manage your databases.

sqlalchemy comes packaged w/ an *ORM* (Object Relational Model) which allows one to manipulate a database as if it were python objects.

**Examples**

.. toctree::
   :maxdepth: 1

   Engine Level Transactions & Rollback w/ pytest <../pytest/pytest_database_transaction/pytest_rollback_after_test>
   Moving Objects Between Sessions <moving_objects_between_sessions>

The Basics of the ORM
---------------------

There's 3 important objects for connecting to a database using sqlalchemy:

engine

  the engine is the core interface to the database , adapted through a dialect that handles the details of the database and the database API

session

  the session is the "handle" for the ORM on the database

declarative base

  the base ORM object that handles mappings between Tables & ORM objects


.. code-block:: python

  from sqlalchemy import create_engine
  from sqlalchemy.ext.declarative import declarative_base

  engine = create_engine('sqlite:///:memory:')

  Base = declarative_base()

  from sqlalchemy import Column, Integer, String
  class User(Base):
      __tablename__ = "users"

      id = Column(Integer, primary_key=True)
      name = Column(String)

  Base.metadata.create_all(engine)  # create all Base-inheriting ORM objects tables on DB

  from sqlalchemy.orm import sessionmaker
  Session = sessionmaker(bind=engine)
  session = Session()

  user1 = User(id=1, name="test_user1")
  session.add(user1)
  session.commit()


And that's all it really takes!

Sure there's more to know about handling Bases, ORM objects, Sessions, etc. But this is really all there is to it!
