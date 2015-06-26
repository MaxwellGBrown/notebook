=======
pyramid
=======

Pyramid is the *microframework* child of ``pylons`` and ``repoze.bfg``. Use it to make your WSGI apps ;).

.. toctree::
  :maxdepth: 1
  :glob:

  examples/*


This page follows the basic construct as outlined in the ``pyramid`` tutorial website. Some more in-depth examples can be found in the TOC above.

A 1-file WSGI app
-----------------

``pyramid`` because it's a *microframework*, supplies us with all the tools we'll need to create our web app and all of the freedom to organize it how we please. In contrast, a traditional framework would say "all of your templates go in ``app/templates`` and all of your controllers go in ``app/controllers``. With ``pyramid`` we can do as we please.

In the 1-file WSGI app below, ``main()`` is constructing the WSGI app and ``hello_world(request)`` is the apps single controller.

pyramid/single_file_app/helloworld.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

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

Running ``python helloworld.py`` will spin up our server and ``main()`` builds and configures the routes of our WSGI app using ``pyramid``. Upon request, the ``hello_world(request)`` controller/function is triggered and returns ``"Hello"`` as it's response.



Packaging applications with pyramid
-----------------------------------

WSGI apps are made to be portable. ``pyramid`` makes packaging apps up easy, and it requires little effort. The minimum requirements for this are:

* having a ``setup.py``
* a basic directory structure 

pyramid/packaging/setup.py
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from setuptools import setup

    requires = [
        'pyramid',
    ]

    setup(name='app_example',
            install_requires=requires,
            entry_points="""\
            [paste.app_factory]
            main = app_example.app:main
            """,
    )

``setup.py``'s job is to create the egg file of our application. This egg file can be used to distribute the application and easy installation. The name of the egg will be ``app_example.egg-info``.

Note that the entrypoint for ``paste.app_factory`` points to ``app_example.app:main``. It's using pythonic module-imports to point to the function ``main()`` in ``app_example/app.py``. When the app is accessed using the egg by things like ``pserve`` which go through the entry point for ``paste.app_factory`` it will provide arguments to ``app_example.app.main()`` and accept it's output to do stuff with. ``app_example.main()`` will be defined a little further down the road...

To complete egg setting up, the application needs to have a ``__init__.py`` file!

pyramid/packaging/app_example/__init__.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  # package

Inside the application package there's going to be the file which creates web server, which mirrors a lot of the functionality of the last examples 1-file-app

pyramid/packaging/app_example/app.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  from wsgiref.simple_server import make_server
  from pyramid.config import Configurator

  def main():
      config = Configurator()
      config.add_route('hello', '/')
      config.scan('views')
      app = config.make_wsgi_app()
      return app

  if __name__ == '__main__':
      app = main()
      server = make_server('localhost', 8888, app)
      print('Starting up server on http://localhost:8888')
      server.serve_forever()

Again, the function of this file is to create a WSGI app and serve it!

Now that we've set it all up, we can build our egg with ``$ python setup develop``.

Note that in this example, we've added ``config.scan('views')``. What's happening here is ``pyramid``'s ``Configurator`` is scanning for any appropriately defined functions that it can use to generate responses. Below is an example of our single view.

pyramid/packaging/app_example/views.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from pyramid.response import Response
    from pyramid.view import view_config

    @view_config(route_name='hello')
    def hello_world(request):
        return Response("Hello")

``views.py`` is leveraging the ``pyramid.view.view_config`` wrapper function to define this function as a view for the path ``'hello'`` which is defined as a route in our ``Configurator`` object in ``app_example/app.py``. 


pyramid and configuration files
-------------------------------

``pyramid`` supplies the tools to work with ``.ini`` files with relative ease.  *I, the author, don't really like* ``.ini`` *files*. In a more formal setting we could absolutely set up the app to run with ``.yaml`` files with a different web server. But, since this is just an example, we'll stick with the suggested ``.ini`` format. 

This example uses the same code as ``pyramid/packaging/`` but instead of using ``pyramid/packaging/app_example/app.py`` to serve the application, this one will use a ``.yaml`` configuration file and ``pserve`` (not a real web server, but good enough for texting).

pyramid/configuration/development.ini
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: ini

::

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


An important note, the ``[app:main]`` section is supposed to lead us to the ``main()`` function that returns our application. We're using the egg to access our app, hence the ``use = egg:app_example``. The naming of ``app_example`` must match the portion of ``setup.py`` where we define the name of the egg ( ``setup(name='app_example`...)``).  

Now that the duty of configuring the application has moved from ``configuration/app_example/app.py`` to the yaml file, we can change the way our app is run. The official ``pyramid`` example claims that many developers put the information to setting up the application in ``configuration/app_example/__init__.py``, but I, *the all powerful author* dislike the idea of this because it implicitly tucks it away. And, after all, **explicit is better than implicit**. 

So, ``configuration/app_example/app.py`` will become ``configuration/app_example/setup_app.py`` as it has now been stripped of the responsibility of setting up and configuring the application

configuration/app_example/setup_app.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: python

::

  from pyramid.config import Configuratior

  def main(global_config, **settings):
      config = Configurator(settings=settings)
      config.add_route('hello', '/')
      config.scan()
      return config.make_wsgi_app()

Now that we have a separated the configuration from the app creation, we can start up the server with ``pserve``

::

  $ pserve development.ini


using templates with pyramid
----------------------------

If you want dynamic content, you're probably going to have to do some templating baby ;). This application builds off of the previous example.

First off we need to tell our ``Configurator`` what type of templating tool we're going to be using. ``pyramid`` suggests we use ``Chameleon``, but no. This is using ``mako`` templates. Note that ``pyramid_mako`` doesn't come standard and needs to be installed with ``$ pip install pyramid_mako``.

templating/app_example/setup_app.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  from pyramid.config import Configurator

  def main(global_config, **settings):
      config = Configurator(settings=settings)
      config.include('pyramid_mako')
      config.add_route('hello', '/')
      config.scan()
      return config.make_wsgi_app()


Well, that was easy. 

Now the view needs to be changed to use a template.

templating/app_example/views.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::
    
    from pyramid.view import view_config

    @view_config(route_name='hello', renderer='templates/hello.mako')
    def hello_wrold(request):
        return dict(title='Hello World')

Yeah, looks werid right? That's because we don't actually render anything in the defined ``view``. Instead, we wrap it with the file we want to render with, and return a ``dict`` that has the arguments to fill that template. The wrapper is also handling turning our HTML into a ``Response`` object, which the earlier examples return. 

The template is going to look something like this:

templating/app_example/templates/hello.mako
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. highlight:: html

::

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


.. highlight:: python

See? We're calling the title there.
