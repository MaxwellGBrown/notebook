.. _pyramid_unittest:

====================
Testing with Pyramid
====================

When testing application code that uses pyramid, there are two main types of tests that can run

**Unit Tests**

  Testing view callables & their returned values *before* they interact with the renderer.

  The application & all of it's pieces *are not* initialized.

**Functional Tests**

  Testing the application using HTTP requests and checking the HTTP response.

  This tests the application and the interaction all of it's pieces.
  

Unit Tests
----------

For unit testing, pyramid provides `pyramid.testing <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/testing.html>`__ to create a test ``Configurator`` object and ``DummyRequest`` objects to pass to view callables.

The dummy ``Configurator`` object returned by ``testing.setUp()`` comes with **none** of the configuration in the application; if any views reference anything in the configuration (e.g. routes) then they need to be added to the dummy config.

``testing.tearDown()`` deconstructs the dummy ``Configurator`` so that a new one can be created.

.. code-block:: python

    import pytest
    import pyramid.testing


    @pytest.fixture
    def test_config(request):
        config = pyramid.testing.setUp()
        request.addfinalizer(pyramid.testing.tearDown)
        return config


    def test_hello_world(test_config):
        from app_example.views import hello_world

        request = pyramid.testing.DummyRequest()
        response = hello_world(request)

        assert response['title'] == "Hello World"


Unit Tests for Views with Permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pyramid.testing`` has a way to handle view callables that require some permission information or the view is locked by permission.

Calling ``config.testing_securitypolicy()`` allows tests to circumvent any pyramid permissions checks.

.. code-block:: python

    test_config.testing_securitypolicy(userid="test", permissive=True)

``testing_securitypolicy`` allows the test to set the userid that's used for authentication.

The value passed as ``permissive`` is whether the user passes or fails any security checks.

.. _pyramid_functional_tests:

Functional Tests
----------------

`Functional testing in pyramid <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/testing.html#creating-functional-tests>`__ is done by building the whole application, sending HTTP request to it, and checking the HTTP responses returned.

Pyramid doesn't have a module for functional tests, but they suggest using pylons project's `WebTest <http://webtest.pythonpaste.org/en/latest/>`__ library.


.. code-block:: python

    import pytest

    from example_app.app_config import main


    @pytest.fixture(scope="class")
    def test_app(request):
        from WebTest import TestApp

        global_config = {
                "__file__": "test.ini",  # the file used to initialize
                "here": "example_ve/example_app",  # the path of the app
                }
        settings = ini_to_dict(ini_filepath, sections=["app:main_app"])

        app = main(global_config, **settings)
        return TestApp(app)


    def test_hello_world(test_app):
        response = test_app.get("/", status=200)
        assert "<h1>Hello World</h1>" in response


The above takes some liberty in passing the necessary items to the app constructor: if an ``.ini`` file is being read for tests see :ref:`ini_to_dict`.


.. note::

    If there are any external dependancies from the application (e.g. database, IMAP server, etc.) then they'll have to have a separate test environment implemented so that functional tests don't interfere with production.

    This can be done by either creating the testing environments or creating fixtures that spoof thier operactions.


Authentication in Pyramids Functional Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since functional tests are operating on the whole application, authentication needs to be sincere. 

What this means is that either:

* A fixture using the ``/login`` feature of the application is set up
* Plant a session cookie in the application using the secret supplied to it in the testing initialization.

The former is easier while the latter is more pure.

Either way the cookies need to be cleared between tests so that the user permissions don't corrupt the next test.

.. code-block:: python

    @pytest.fixture(scope="function")
    def as_user(request, test_app):
        params = {"login": "test_user", password: "password1"}
        response = test_app.post("/login", params=params)
        if "Login Failed" in response.text:
            raise Exception("Login failed. Fixture compromised.")

        def clear_cookies():
            test_app.reset()
        request.addfinalizer(clear_cookies)

        return "test_user"


    def test_hello_world(test_app, as_user)
        response = test_app.get("/")
        expected_greeting = "Hello " + as_user
        assert expected_greeting in response.text
