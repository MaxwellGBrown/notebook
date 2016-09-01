.. _pyramid_auth:

======================================
Pyramid Authentication & Authorization
======================================

Authentication & Authorization are important features for web applications. They allow one to restrict access to certain pages based on the authenticated users authorization.

While both are closely related (and can be abbreviated as 'auth'), Authentication & Authorization have important distinctions:

**Authentication**

    Identity verification; are you who you say you are?

**Authorization**

    Permission verification; are you allowd access to what you're attempting to access?

The basic steps we'll take to set up both Auths:

#. Basic User ORM model
#. Authentication Policy
#. Authorization Policy
#. Defining ``request.user``
#. Create login/logut views
#. Assign permissions to views
#. Defining a "403 Forbidden" view
#. Testing w/ Auth Policies


Defining Basic User Model
-------------------------
The foundation for authentication is a model for users to authenticate themselves as.

This basic user model defines usernames, passwords, and user_ids.

The user's password is salted & hashed so that it's not stored in the database as plain text.

For more on how to properly store & manage passwords see `crackstation's hashing-security <https://crackstation.net/hashing-security.htm>`__ page.

.. code-block:: python

    # auth_app/models/auth.py
    from hashlib import sha1
    import os

    from sqlalchemy import Column, Unicode, Integer
    from sqlalchemy.ext.hybird import hybrid_property

    from auth_app.model import Base


    class User(Base):
        __tablename__ = "user"

        user_id = Column(Integer, autoincrement=True, primary_key=True)
        username = Column(Unicode(32), unique=True)
        _password = Column('password', Unicode(255))  # @property = .password

        @hybrid_property
        def password(self):
            return self._password

        @password.setter
        def set_password(self, password):
            # password arg is assumed UTF-8
            salt = sha1(os.urandom(40))
            salted_pwd = password + salt.hexdigest()
            sha1_hash = sha1(salted_pwd.encode("UTF-8"))
            self._password = salt.hexdigest() + sha1_hash.hexdigest()

        def validate(self, password):
            """ Returns True if `password` matches unhashed User._password """
            combined_password = password + self.password[:40]
            hashed_password = sha1(combined_password.encode("UTF-8"))
            passwords_match = self.password[40:] == hashed_password.hexdigest()
            return passwords_match


Using ``@hybrid_property``, an interface for the hashed ``User._password`` column is provided.

This allows ``User.password`` to operate just like the standard ``@property`` wrapper.


Authentication Policy
---------------------
Now that the user model is defined, an authentication policy can be included.

This example highlights ``AuthTktAuthenticationPolicy`` from ``pyramid.authentication``. 

``AuthTktAuthenticationPolicy`` relies on a function that, when passed a userid & request, returns a list of :ref:`principals <authz_ace>` for the currently authenticated user, or ``None`` if there isn't an authenticated user.

.. _authn_principal:
.. code-block:: python

    # auth_app/models/auth.py
    from pyramid.security import unauthenticated_userid

    def auth_callback(userid, request):
        """ AuthTktAuthenticationPolicy(..., callback=auth_callback, ...) """
        userid = unauthenticated_userid(request)
        if userid is None:
            return None

        user = Session.query(User).filter_by(user_id=userid).first()
        if user is not None:
            list_of_principals = list()
            # ADD PRINCIPALS HERE
            return list_of_principals
        else:
            return None

Using this callback, the authentication policy can be defined in the app config

.. code-block:: python

    # auth_app/app_config.py
    from pyramid.config import Configurator
    from pyramid.authentication import AuthTktAuthenticationPolicy

    from auth_app.model.auth import user_callback

    def main(global_config, **settings):
        config = Configurator(settings=settings)
        ...
        authn_policy = AuthTktAuthenticationPolicy(
                "auth_secret",  # should come from .ini or config
                callback=user_callback,
                hashalg='sha512',
        )
        config.set_authentication_policy(authn_policy)
        ...
        return config.make_wsgi_app()


Authorization Policy
--------------------
pyramid comes packaged with a single predefined authorization policy: ``ACLAuthorizationPolicy``.

ACLAuthorization comes with two important definitions:

**ACL: Access Control List**

  A sequence of ACE tuples

  Defined as ``__acl__`` in any pyramid `resource <http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource>`__

.. _authz_ace:

**ACE: Access Control Entry**

  A single element in the ACL that's composed of 3 things:

  1. Action (``Allow`` or ``Deny`` from ``pyramid.security``)
  2. Principal (a string/object describing a user or group)
  3. Permission (a string describing the permission granted from the ACE)

It's the authorization policy's job to match the principals from the auth policy's :ref:`callback <authn_principal>` to permissions used by view callables.

ACL's are composed of all the ``__acl__`` properties of each resource found during :ref:`resource location <url_dispatch_resource_location>`.

To supply a default set of ACL's, a RootFactory with the ``__acl__`` property must be defined.

.. code-block:: python

    # auth_app/security/factory.py
    from pyramid.security import Allow, Everyone, Authenticated

    class RootFactory(object):

        __acl__ = [
                (Allow, Authenticaed, "view"),
                (Allow, "admin", "admin"),
                ]

        def __init__(self, request):
            self.request = request


Note that instead of supplying a string as a principal you can also supply the special principals ``Everyone`` and ``Authenticated`` from ``pyramid.security`` which are exactly what they sound like.

Assigning ``ACLAuthorizationPolicy`` to the ``Configurator`` completes the basic setup of the authorization policy.

.. code-block:: python

    #auth_app/app_config.py
    from pyramid.config import Configurator
    from pyramid.authorization import ACLAuthorizationPolicy

    from auth_app.security.factory import RootFactory

    def main(global_config, **settings):
        config = Configurator(settings=settings)
        ...
        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)

        config.set_root_factory(RootFactory)
        ...
        return config.make_wsgi_app()


.. note::

    Since route-specific factories replace RootFactory, RootFactory's ACL does *not* get included in that route's total ACL!


Defining request.user
---------------------
While completely optional, it's a good idea to define ``request.user`` as the currently authenticated user.

This'll keep the views clean from current user lookup & make unit testing much easier.

Start by defining a function to extend request.

.. code-block:: python

    # auth_app/models/auth.py
    from pyramid.security import unauthenticated_userid

    def request_user(request):
        """ config.add_request_method(request_user, "user", reify=True) """
        userid = unauthenticated_userid(request)
        if userid is not None:
            user = Session.query(User).filter_by(user_id=userid).first()
            return user
        else:
            return None


Now that an interface for ``request.user`` is defined, the property itself can be defined.

.. code-block:: python

    # auth_app/app_config.py
    from auth_app.model.auth import request_user

    def main(global_config, **settings):
        ...
        config.add_request_method(request_user, 'user', reify=True)
        ...
        return config.make_wsgi_app()

Note that ``reify=True`` just means that the return value of ``request_user`` is cached, and the function is not called any time after the first.


Creating login/logout views
---------------------------
With both auth policies in place, users can be provided with login/logout pages to authenticate.

Remembering authenticated users is done by managing their cookies using ``remember`` and ``forget`` from ``pyramid.security``. These are both pointers to the application's authentication policy's implementation.


.. code-block:: python

    # auth_app/views/auth.py
    from pyramid.view import view_config, view_defaults
    import pyramid.httpexceptions as http
    from pyramid.security import remember, forget

    from auth_app.models.auth import UserMgr

    @view_defaults(route_name="login", renderer="login.mako")
    class LoginViews(object):

        def __init__(self, request):
            self.request = request

        @view_config(request_method="GET")
        def get_login(self):
            return {}

        @view_config(request_method="POST")
        def post_login(self):
            user = UserMgr.one(request.POST.get('username'))
            if user is not None:
                if user.validate(request.POST.get('password')) is True:
                    headers = remember(self.request, user.user_id)
                    home_url = request.route_url('home')
                    raise http.HTTPFound(home_url, headers=headers)
            return self.get_login()

    @view_config(route_name="logout")
    def logout(request):
        headers = forget(request)
        return HTTPFound(request.route_url('login'), headers=headers)


For more encompassing views & better validation, check out the full code for auth_app's :download:`views/auth.py <auth_app/views/auth.py>`.


Assign Permissions To Views
---------------------------
Permissions can be assigned to views using ``@view_config`` and ``@view_defaults``.

Remember, permissions are the 3rd item in :ref:`ACE tuples <authz_ace>` which are matched to users with principals given to them from the authentication policy's :ref:`callback <authn_principal>`.


.. code-block:: python
    :emphasize-lines: 4

    from pyramid.view import view_config

    @view_config(route_name="home", renderer="home.mako",
            permission="view",
            )
    def home(request):
        return {}

Anybody attempting to view this page without the *permission* ``"view"`` will be served a 403 Forbidden page.


Defining a "403 Forbidden" view
-------------------------------
Anybody who isn't authorized to access a view callable will be served an HTTP "403 Forbidden" error.

Pyramid allows the definition of custom 403 views using ``@forbidden_view_config``, which is nearly-identical to ``@view_config``.

.. code-block:: python

    # auth_app/views/forbidden.py
    from pyramid.view import forbidden_view_config

    @forbidden_view_config(renderer="forbidden.mako")
    def forbidden(request):
        return {"message": "You are not authorized to access this page"}

More on the "forbidden view hook" can be found in `pyramids docs <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#changing-the-forbidden-view>`__.


Testing with Auth Policies
--------------------------
After adding auth policies, unit tests and functional tests must now be able to handle both.

These examples will be leveraging `pytest`.


Unittests w/ Auth Policies
++++++++++++++++++++++++++

For unittests, pyramid has a baked in method to grant all permissions.

.. code-block:: python

    # auth_app/tests/test_views.py
    import pyramid.testing
    import pytest

    @pytest.fixture
    def test_config(request):
        config = pyramid.testing.setUp()

        request.addfinalizer(pyramid.testing.tearDown)
        return config

    @pytest.fixture
    def test_user(request):
        class DummyUser(object):
            username = "testuser"
            password = "hunter2"

            @staticmethod
            def validate():
                return True

        return DummyUser

    def test_permissive_home_view(test_config, test_user):
        from auth_app.views.home import home
        test_config.testing_sercuritypolicy(userid="1", permissive=True)

        request = testing.DummyRequest()
        request.user = test_user

        assert home(request)

Make note that setting ``request.user`` is only required if the ``request.user`` method is in use.


Fxnal tests w/ Auth Policies
++++++++++++++++++++++++++++
Requiring authentication puts a decent strain on functional tests.

Fortunately, the developer has all the code used to create auth cookies at their hands; it just requires jumping through some hoops.

To begin, the Authentication policy needs to either be separated from app_config.py or identically re-created in a test fixture.

.. code-block:: python

    # auth_app/tests/test_fxnal.py
    import pytest

    from auth_app.model.auth import user_callback

    @pytest.fixture(scope="function")
    def as_test_user(request, init_app, test_app, test_user):
        pyramid_cfg = ini_to_dict("test.ini")  # read ini as dict
        auth_cfg = {k[5:]: v for k, v in pyramid_cfg.items() if k[:5] == "auth."}

        # re-create the auth policy as in app_config
        from pyramid.authentication import AuthTktAuthenticationPolicy
        authn_policy = AuthTktAuthenticationPolicy(
                "auth_secret", callback=user_callback, hashalg='sha512')

        # use app's auth policy to create a cookie
        environ = {  # required by auth policy's "CookieHelper"
                "REMOTE_ADDR": "0.0.0.0",
                "SERVER_NAME": "localhost",
                "SERVER_PORT": "9999",
                }
        http_request = init_app.request_factory(environ)
        headers = authn_policy.remember(http_request, test_user.user_id)

        # strip "cookie_name=" from Set-Cookie header value
        set_cookie = headers[0][1]
        cookie = set_cookie[len(auth_cfg['cookie_name'] + "="):]

        # save the cookie in the application
        test_app.set_cookie(auth_cfg['cookie_name'], cookie)

        # remove the cookie on fixture teardown
        return test_user

The ``init_app`` and ``test_app`` fixtures initialize the WSGI app and return a ``webtest.TestApp`` object respectively.

``test_user`` is a fixutre that returns a User model in the application to authenticate as.

Also note that this fixture assumes that all of the authn policy's kwargs are supplied in the .ini configuration with the prefix ``auth.``.


