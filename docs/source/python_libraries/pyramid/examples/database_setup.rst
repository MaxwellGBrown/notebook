=====================
Setting up a database
=====================

-----------------------------
creating an application model
-----------------------------

Coming soon...

---------------------------------------------
initializing database on application creation
---------------------------------------------

It's often very frustrating to have the user setup the database in some sort of way before running the application.

Using ``pyramid.events``, the applicaiton can force the creation of the model when the WSGI application is created.

In the application setup/entry point, add code that will handle event listeners for application creation.

.. code-block:: python

    from pyramid.events import ApplicaitonCreated
    from pyramid.events import subscriber

    @subscriber(ApplicationCreated)
    def create_database_with_application(event):
        print("Initializing database...")
        settings = event.app.registry.settings  # get .ini settings
        # create the database!
