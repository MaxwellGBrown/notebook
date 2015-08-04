========================
Pylons-style controllers
========================

Pyramid is void of terminology relating to the **controller** of the previous pylons implementation. However, there is often a need to group logically related views. This example will cover grouping views into python classes, essentially making a formal controller.

Setting up the views
--------------------

To group logically related views into a class there are two decorators that can be leveraged from ``pyramid.view``. ``view_config``, a class decorator, and ``view_defaults``.

controllers/app_example/views.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyramid.view import view_config, view_defaults

    @view_defaults(renderer='templates/home.mako')
    class AppExampleViews(object):
        def __init__(self, request):
            self.request = request

        @view_config(route_name='home')
        def home(self):
            return {'name': "Home View"}

        @view_config(route_name='hello')
        def hello(self):
            return {'name': "Hello View"}


The decorators controll how our new ``class`` view interacts with the app ``Configurator``. 

``view_defaults()`` is a ``class`` decorator that sets the defaults for all of the class methods that are used as views. In this example, ``view_defaults(renderer='templates/home.mako')`` sets the default template for all of the view methods.

``view_config()`` is a ``function`` decorator that sets the information for that method/view. In the example above, ``route_name`` is being defined which matches up to the routes defined in the ``Configurator``. ``view_config()`` overrides any default settings set in ``view_defaults()``.



Changing the Configurator for Controllers
-----------------------------------------

Because there are multiple views now, there needs to be additional routes in the ``Configurator`` in ``app_example/setup_app.py``

controllers/app_example/setup_app.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pyramid.config import Configurator


    def main(globall_config, **settings):
        config = Configurator(settings=settings)
        config.include('pyramid_mako')
        config.add_route('home', '/')
        config.add_route('hello', '/howdy')
        config.scan('.views')
        return config.make_wsgi_app()


Now in the ``Configurator`` there are two defined routes that match the routes defined by the ``view_config()`` decorators:

* visiting the ``/`` route will render ``AppExampleViews.home()``
* visiting the ``/howdy`` route will render ``AppExampleViews.hello()``


The default template for the Controller
---------------------------------------

/templates/home.mako is the template that is shared in the Controller as defined by the class decorator ``view_defaults()``. This is the template that matches that controller.

controllers/app_example/templates/home.mako
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    <html>
    <head>
        <title>${name}</title>
    </head>
    <body>
    <div>
        <h1>Hi ${name}</h1>
    </div>
    </body>
    </html>



nosetests for the Controller
----------------------------

Setting up nosetests to work with Controller style views requires a little extra work. Instead of running a request through a view function, the Controller class needs to be initialized with the request and then the view method needs to be called.

controllers/app_example/tests.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import unittest

    from pyramid import testing

    class AppExampleViewTests(unittest.TestCase):
        def setUp(self):
            self.config = testing.setUp()

        def tearDown(self):
            testing.tearDown()

        def test_home(self):
            from .views import AppExampleViews

            request = testing.DummyRequest()
            controller = AppExampleViews(request)
            response = controller.home()
            self.assertEqual("Home View", response['name']

        def test_hello(self):
            from .views import AppExampleViews

            request = testing.DummyRequest()
            controller = AppExampleViews(request)
            response = controller.hello()
            self.assertEqual("Hello View", response['name'])


    class AppExampleFunctionalTests(unittest.TestCase):
        def setUp(self):
            from app_example.setup_app import main
            app = main({})
            from webtest import TestApp

            self.testapp = TestApp(app)

        def test_home(self):
            response = self.testapp.get('/', status=200)
            self.assertIn(b'<h1>Hi Home View</h1>', response.body)

        def test_hello(self):
            response = self.testapp.get('/howdy', status=200)
            self.assertIn(b'<h1>Hi Hello View</h1>, response.body')
