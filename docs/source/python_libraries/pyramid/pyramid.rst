=======
pyramid
=======

Pyramid is the *microframework* child of ``pylons`` and ``repoze.bfg``. Use it to make your WSGI apps ;).

.. toctree::
  :maxdepth: 1
  :glob:

  examples/*


Below demonstrates the setup of a basic web app.

Hello World in 1 File
---------------------

``pyramid`` is a *microframework*, supplies all the tools one may need to create a web app and all of the freedom to organize it how we please. 

In the 1-file WSGI app below, ``main()`` is constructing the WSGI app and ``hello_world(request)`` is the apps single view.


.. code-block:: python
    :caption: pyramid/single_file_app/helloworld.py

    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from pyramid.response import Response

    def hello_world(request):
        return Response('Hello')

    def main():
        config = Configurator()
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
        return app

    if __name__ == '__main__':
        app = main()
        server = make_server('0.0.0.0', 6547, app)
        print ('Starting up server on http://localhost:6547')
        server.serve_forever()

Running ``python helloworld.py`` will spin up the server and ``main()`` builds and configures the routes of the WSGI app using ``pyramid``. Upon request, the ``hello_world(request)`` controller/function is triggered and returns ``"Hello"`` as it's response.



Pyramid & Eggs
--------------

WSGI apps are made to be portable. ``pyramid`` makes packaging apps up easy, and it requires little effort. The minimum requirements for this are:

* having a ``setup.py`` that uses ``setuptools.setup()`` to build entry points
* a basic python directory structure with ``__init__.py`` files.


.. code-block:: python
    :caption: pyramid/packaging/setup.py

    from setuptools import setup

    requires = [
        'pyramid',
    ]

    setup(name='app_example',
            install_requires=requires,
            entry_points="""\
            [paste.app_factory]
            main = app_example.setup_app:main
            """,
    )

``setup.py``'s job is to create the egg file of our application. This egg file can be used to distribute the application and easy installation. The name of the egg will be ``app_example.egg-info``.

The entrypoint for ``paste.app_factory`` points to ``app_example.setup_app:main``. It's using pythonic module-imports to point to the function ``main()`` in ``app_example/setup_app.py``. When the app is accessed using the egg by things like ``pserve``, which go through the entry point for ``paste.app_factory``, it will provide arguments to ``app_example.app.main()`` and accept it's output to do stuff with. ``app_example.main()`` will be defined a little further down the road...



The ``pyramid`` developers suggest putting ``main()`` in the ``__init__.py`` file for the application. It can be wherever one wants it to be as long as the route matches the call in the ``setup.py`` file.

Either way, the application needs an ``__init__.py`` for pythonic imports!


.. code-block:: python
    :caption: pyramid/packaging/app_example/__init__.py

  ## if setup.py's entryway was app_example:main, this is what it would be for
  ##
  ## either way, the __init__.py file is needed for pythonic imports!
  # from pyramid.config import Configurator
  #
  # def main():
  #     config = Configurator()
  #     config.add_route('hello', '/')
  #     config.scan('views')
  #     app = config.make_wsgi_app()
  #     return app



In this example, since ``setup.py`` points to ``app_example.setup_app:main``, the ``main()`` function, which returns the WSGI app, needs to be defined.


.. code-block:: python
    :caption: pyramid/packaging/app_example/setup_app.py

  from pyramid.config import Configurator

  def main():
      config = Configurator()
      config.add_route('hello', '/')
      config.scan('views')
      app = config.make_wsgi_app()
      return app

Again, the function of this file is to create a WSGI app and serve it!

With ``main()``'s call to ``Configurator.make_wsgi_app()`` an egg can be created by typing ``$ python setup.py develop``.



Note that ``config.add_view()`` has been replaced with ``config.scan()``. This scans the file ``.views`` for any defined views.


.. code-block:: python
    :caption: pyramid/packaging/app_example/views.py

    from pyramid.response import Response
    from pyramid.view import view_config

    @view_config(route_name='hello')
    def hello_world(request):
        return Response("Hello")

``views.py`` is leveraging the ``pyramid.view.view_config`` wrapper function to define this function as a view for the path ``'hello'`` which is defined as a route in our ``Configurator`` object in ``app_example/setup_app.py``. 

Using ``Configurator.scan('views')``, this file is scanned for any views defined by appropriate ``pyramid.view`` wrappers.



Configuration (.ini) files
--------------------------

Python's WSGI apps are traditionally served using ``.ini`` files (boooo!).

The ``.ini`` file works in conjunction with pyramid's ``pserve`` command, which can be used to serve pyramid WSGI apps.


.. code-block:: ini
    :caption: pyramid/configuration/development.ini

    [app:main]
    use = egg:app_example
    pyramid.reload_templates = true
    
    [server:main]
    use = egg:pyramid#wsgiref
    host = 0.0.0.0
    port = 6547
    
    [loggers]
    keys = root
    
    [handlers]
    keys = console
    
    [formatters]
    keys = generic
    
    [logger_root]
    level = INFO
    handlers = console
    
    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic
    
    [formatter_generic]
    format = %(asctime)s %(levelname)-5.5s [%(name)s][%(threadName)s] %(message)s

``[app:main]`` refers to the egg created from ``setup.py`` where ``main`` refers to ``entry_points="[paste.app_factory] main = app_example.setup_app:main``. Remember, that exact line is referring the function in the app that returns the WSGI app. 

``use = egg:app_example`` refers to what the egg is named in the ``setup.py``. In this continued example it's ``name="app_example"``.



Now that we have a separated the configuration from the app creation, we can start up the server with ``pserve``

::

  $ pserve development.ini



Mako Templates & Pyramid
------------------------

Pyramid comes packed with ``chameleon``. ``jinja2``, and ``mako``. This example will use ``mako``. 

First, ``setup.py`` needs to be updated to require the templating tool.


.. code-block:: python
    :caption: templating/setup.py

    from setuptools import setup

    requires = [
        'pyramid',
        'pyramid_mako',  # newly added
    ]

    setup(name='app_example',
          install_requires=requires,
          entry_points="""\
          [paste.app_factory]
          main = app_example.setup_app:main
          """,
     )

After that, the application ``Configurator`` needs to know the templating tool being used. Note that ``pyramid_mako`` doesn't come standard and needs to be installed with ``$ pip install pyramid_mako``.


.. code-block:: python
    :caption: templating/app_example/setup_app.py

  from pyramid.config import Configurator

  def main(global_config, **settings):
      config = Configurator(settings=settings)
      config.include('pyramid_mako')
      config.add_route('hello', '/')
      config.scan()
      return config.make_wsgi_app()



Now the view needs to be changed to use a template.


.. code-block:: python
    :caption: templating/app_example/views.py
    
    from pyramid.view import view_config

    @view_config(route_name='hello', renderer='templates/hello.mako')
    def hello_wrold(request):
        return dict(title='Hello World')


Since the app now uses ``pyramid_mako`` to render responses, instead of sending the content from the ``view`` to the client, the ``view`` sends the template (defined in ``view_config(renderer='templates/hello.mako')`` the blocks of information needed to render the page's content.


.. code-block:: html
    :caption: templating/app_example/templates/hello.mako

    <html>
    <head>
        <title>${title}</title>
    </head>
    <body>
    <div>
        <h1>${title}</h1>
    </div>
    </body>
    </html>

Alternatively, one could render the template and return a ``Response`` object instead of linking the ``view`` to a template in ``view_config``.
