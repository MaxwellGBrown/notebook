=====================
Setting up a database
=====================

Web applications like databases. Here's the real-quick on setting one up w/ an
application!

Defining the Model
------------------

First, we'll start by defining model files in ``database_app/models/``. To
start defining an ORM we'll need a few ORM objects: a ``scoped_session``, and a
``declarative_base``

.. code-block:: python
    :caption: database_app/models/__init__.py

    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import scoped_session, sessionmaker


    Session = scoped_session(sessionmaker())
    Base = declarative_base()

    """ import objects as part of ``import database_models as app_model`` """
    from database_app.models.contact import Contact


    def bind_engine(engine, create_all=False):
        """ binds engine to Session & Base.metadata """
        Session.configure(bind=engine)
        Base.metadata.bind = engine
        if create_all is True:
            Base.metadata.create_all(engine)


Note that ``database_app/models/__init__.py`` imports a contact model that
hasn't been defined yet. That's next.

The reason that it's imported like that is so, instead of just importing the
parts of the model we want::

    from database_app.models.contact import Contact
    from database_app.models import Session

    Session.query(Contact).all()

We can get all the parts of the model we want by importing
``database_app.models``::

    import database_app.models as app_model

    app_model.Session.query(app_model.Contact).all()


So now that we've estabilshed the why, let's execute the what.

.. code-block:: python
    :caption: Contact model from database_app/models/contact.py

    from sqlalchemy import Column, Integer, Unicode

    from database_app.models import Base, Session


    class Contact(Base):
        """ an example ORM object """
        __tablename__ = "contact"

        id = Column(Integer, primary_key=True)
        first_name = Column(Unicode)
        last_name = Column(Unicode)
        address = Column(Unicode)


Linking the Model to the App
----------------------------

Now that a model is defined, it needs to be leveraged by the application.

To start, we'll define our DB connection in our ``.ini`` file.

:: 

    [app:main]
    ...
    sqlalchemy.url = sqlite:///database_app.sqlite
    ...

This supplies the application with the database connector string we'll use to
create an engine.

Speaking of engines, since we have an ``.ini`` file, we can use
sqlalchemy's
`engine_from_config <http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#sqlalchemy.engine_from_config>`__ to create an engine.

Also, we'll use ``database_app.models.bind_engine`` to bind it to ``Base`` &
``Session``.

.. code-block:: python
    :caption: create & bind engine in app_config.py

    from pyramid.config import Configurator
    from sqlalchemy import engine_from_config

    import database_app.models as app_model


    def main(global_config, **settings):
        config = Configurator(settings=settings)
        ...
        # config.scan('database_app.models')
        engine = engine_from_config(configuration=settings, prefix="sqlalchemy.")
        app_model.bind_engine(engine, create_all=True)
        ...
        return config.make_wsgi_app()


After binding the engine, all of the ORM objects will interact w/ the database!

.. note::
    `Pyramid swears on "scanning" the models before importing them <http://docs.pylonsproject.org/projects/pyramid_cookbook/en/latest/database/sqlalchemy.html#importing-all-sqlalchemy-models>`__
    to avoid circular import of ``Base`` & ``Session``. However, I haven't
    noticed anything different.


Using the Model in Views
------------------------

Typically *manager* classes are defined to handle sessions & ORM objects so
that the view doesn't have to worry about any of that. 

But that's much more than is needed for this example ;)

.. code-block:: python
    :caption: using app_model in view callables

    from pyramid.view import view_config

    import database_app.models as app_model


    @view_config(route_name="index", renderer="index.mako")
    def hello_world(request):
    form = ContactForm(request.POST)
    if request.method == "POST" and form.validate():
        contact = app_model.Contact(**form.data)
        app_model.Session.add(contact)
        app_model.Session.commit()
    all_contacts = app_model.Session.query(app_model.Contact).all()
    return {"form": form, "contacts": all_contacts}
