.. _alembic:

=======
alembic
=======

alembic is a revision control package for sqlalchemy based models. Use it to maintain sqlalchemy implementations!

Alembic allows developers to create database migrations, branches, and "versions" to allow upgrading/downgrading along branches to maintain database integrity.

::

  $ cd <project_name>
  $ alembic init alembic

This will create an ``./alembic/`` directory & ``./alembic.ini`` which is responsible for maintaining alembic.


To begin a new revision...

::
  
  $ alembic revision -m "message for new version"


Also, alembic can automatically read sqlalchemy ORM models that inherit from *declarative Base*, and compare revisions to handle changes::

  $ alembic revision --autogenerate -m "autodetect changes to ORM inheriting Base"

This will generate a new version with changes. It's not perfect though, and you should review these changes.

To upgrade/downgrade between versions...

::

  $ alembic upgrade <version or head>
  $ alembic downgrade <version or base>
