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

To successfully spoof the cookies provided by the application's authentication
policy, it needs to be separated from the Configurator's initiation.

.. code-block:: python

    # app_config.py 

    import .auth as app_auth

    def main(global_config, **settings):
        config = Configurator(...)

        ...

        # read auth. from configuration
        auth_cfg = {k[5:]: v for k, v in settings.items() if k.startswith('auth.')}
        # initiate authentication policy
        authn_policy = app_auth.authn_policy(callback=..., **auth_cfg)
        config.set_authentication_policy(authn_policy)

        # initiate authorization policy
        authz_policy = app_auth.authz_policy(**auth_cfg)
        config.set_authorization_policy(authz_policy)

        ...

        return config.make_wsgi_app()


Moving both auth policies to **auth.py** is straightforward: they're just
wrapped in their basic functions.

.. code-block:: python

    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy


    def authn_policy(*args, **kwargs):
        return AuthTktAuthenticationPolicy(*args, **kwargs)


    def authz_policy(*args, **kwargs):
        return ACLAuthorizationPolicy()


After splitting out the auth policies, a fixture can use them to create
authentication headers/cookies using the same configuration values the
application is using to create them.

.. code-block:: python

    @pytest.fixture(scope="function")
    def as_user(request, settings, test_app, test_user):
        auth_cfg = {k[5:]: v for k, v in settings.items() if k.startswith('auth.')}
        authn_policy = app_auth.authn_policy(callback=..., **auth_cfg)

        # use the app's auth policy to create the cookie
        environ = {  # required by auth policy's "CookieHelper"
                "REMOTE_ADDR": "0.0.0.0",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": "9999",
                }
        auth_request = test_app.app.request_factory(environ)
        headers = authn_policy.remember(auth_request)

        # strip "cookie_name=" from Set-Cookie header value
        cookie_name = auth_cfg.get("cookie_name", "auth_tkt")
        set_cookie = headers[0][1]
        cookie = set_cookie[len(cookie_name + "="):]

        # save the cookie in the app
        test_app.set_cookie(cookie_name, cookie)

        request.finalizer(test_app.app.reset)  # clear cookies on teardown
        return test_user


    def test_hello_world(test_app, as_user)
        response = test_app.get("/")
        expected_greeting = "Hello " + as_user.username
        assert expected_greeting in response.text
