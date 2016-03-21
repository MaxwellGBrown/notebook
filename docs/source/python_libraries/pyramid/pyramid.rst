.. _pyramid:

=======
pyramid
=======

Pyramid is the *microframework* child of ``pylons`` and ``repoze.bfg``. Use it to make your WSGI apps ;).

**Examples**

.. toctree::
  :maxdepth: 1

  pyramid_templating/pyramid_templating
  pyramid_controllers/pyramid_controllers
  pyramid_unittests/pyramid_unittests
  pyramid_database_setup/pyramid_database_setup
  form_as_separate_template/form_as_separate_template 
  pyramid_simple_ajax/pyramid_simple_ajax
  Inline Edits with X-Editable <validating_inline_edits/validating_inline_edits>
  AJAX Tables with DataTables <pyramid_datatables_ajax/pyramid_datatable>

  
----------
The Basics
----------

Below demonstrates the setup of a basic web app.

Hello World in 1 File
---------------------

``pyramid`` is a *microframework*, supplies all the tools one may need to create a web app and all of the freedom to organize it how we please. 

In the 1-file WSGI app below, ``main()`` is constructing the WSGI app and ``hello_world(request)`` is the apps single view.


.. literalinclude:: pyramid_single_file_app/single_file_app.py
    :language: python
    :caption: a simple single file web app


Running ``python helloworld.py`` will spin up the server and ``main()`` builds and configures the routes of the WSGI app using ``pyramid``. Upon request, the ``hello_world(request)`` controller/function is triggered and returns ``"Hello"`` as it's response.



Pyramid & Eggs
--------------

WSGI apps are made to be portable. ``pyramid`` makes packaging apps up easy, and it requires little effort. The minimum requirements for this are:

* having a ``setup.py`` that uses ``setuptools.setup()`` to build entry points
* a basic python directory structure with ``__init__.py`` files.


.. literalinclude:: pyramid_basic_app/setup.py
    :language: python
    :caption: a basic pyramid setup.py
    :emphasize-lines: 8, 12

``setup.py``'s job is to create the egg file of our application. This egg file can be used to distribute the application and easy installation. The name of the egg will be ``basic_app.egg-info``.

The entrypoint for ``paste.app_factory`` points to ``basic_app.setup_app:main``. It's using pythonic module-imports to point to the function ``main()`` in ``basic_app/setup_app.py``. When the app is accessed using the egg by things like ``pserve``, which go through the entry point for ``paste.app_factory``, it will provide arguments to ``basic_app.app.main()`` and accept it's output to do stuff with. ``basic_app.main()`` will be defined a little further down the road...



The ``pyramid`` developers suggest putting ``main()`` in the ``__init__.py`` file for the application. It can be wherever one wants it to be as long as the route matches the call in the ``setup.py`` file.

Either way, the application needs an ``__init__.py`` for pythonic imports!


.. literalinclude:: pyramid_basic_app/basic_app/__init__.py
    :language: python
    :caption: a pyramid webapp's __init__.py


In this example, since ``setup.py`` points to ``basic_app.setup_app:main``, the ``main()`` function, which returns the WSGI app, needs to be defined.


.. literalinclude:: pyramid_basic_app/basic_app/setup_app.py
    :language: python
    :caption: point the setup.py to app creation function


Again, the function of this file is to create a WSGI app and serve it!

With ``main()``'s call to ``Configurator.make_wsgi_app()`` an egg can be created by typing ``$ python setup.py develop``.



Note that ``config.add_view()`` has been replaced with ``config.scan()``. This scans the file ``.views`` for any defined views.


.. literalinclude:: pyramid_basic_app/basic_app/views.py
    :language: python
    :caption: simple views setup for pyramid


``views.py`` is leveraging the ``pyramid.view.view_config`` wrapper function to define this function as a view for the path ``'hello'`` which is defined as a route in our ``Configurator`` object in ``basic_app/setup_app.py``. 

Using ``Configurator.scan('views')``, this file is scanned for any views defined by appropriate ``pyramid.view`` wrappers.



Configuration (.ini) files
--------------------------

Python's WSGI apps are traditionally served using ``.ini`` files (boooo!).

The ``.ini`` file works in conjunction with pyramid's ``pserve`` command, which can be used to serve pyramid WSGI apps.


.. literalinclude:: pyramid_basic_app/development.ini
    :language: ini
    :caption: basic pyramid app .ini file


``[app:main]`` refers to the egg created from ``setup.py`` where ``main`` refers to ``entry_points="[paste.app_factory] main = basic_app.setup_app:main``. Remember, that exact line is referring the function in the app that returns the WSGI app. 

``use = egg:basic_app`` refers to what the egg is named in the ``setup.py``. In this continued example it's ``name="basic_app"``.



Now that we have a separated the configuration from the app creation, we can start up the server with ``pserve``

::

  $ pserve development.ini


With our .ini and setup.py creating an egg, this application can be run on most web servers!
