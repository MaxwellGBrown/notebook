======================================
Pyramid Authentication & Authorization
======================================

Authentication & Authorization are important features for web applications. They allow one to restrict access to certain pages based on their authorization.

While both are closely related (and can be abbreviated as 'auth'), Authentication & Authorization have important distinctions:


**Authentication**

    Identity verification; are you who you say you are?

**Authorization**

    Permission verification; are you allowd access to what you're attempting to access?

The basic steps we'll take to set up both Auths:

1. Create a User/Principal model
2. Create a ``get_user`` fxn & add as ``request.user`` member
3. Create a "groupfinder" to return a users principals
4. Create a ``RootFactory`` to assign permissions
5. Add Authorization & Authentication policies to ``Configurator``
6. Create login/logout views using ``pyramid.security``'s ``remember`` &
   ``forget``
7. Assign ``permission`` as a kwarg to protected view callables.


Authentication
--------------

Pyramid provides a few different authentication policies/helpers. This example uses ``pyramid.authentication.AuthTktAuthenticationPolicy``.


Defining Users & Groups/Principals
++++++++++++++++++++++++++++++++++

Before defining any interactions between the Authentication policy & the
application, the concept of a "user" & "groups" or "principals" needs to be
defined.

Typically users & their groups would be defined by some sort of ORM definition
so they can be stored in a database. However, *this is not a requirement*!

Based on the example "auth_app" (python_libraries/pyramid/pyramid_authentication), here's an example of a non-orm database user definition.


.. code-block:: python
    :caption: auth_app/model/auth.py demonstrates a User object

    class User(object):

        def __init__(self, userid, username, password, user_type="user"):
            self.userid = userid
            self.username = username
            self.password = password
            self.user_type = user_type
            if self.user_type == "admin":
                self.groups = ["group:admin"]
            else:
                self.groups = ['group:user']

    USERS = [  # this is the user "database"
            User(1, "admin_user", "hunter2", "admin"),
            User(2, "normal_user", "password1", "user"),
            ]

In the above example, ``USERS`` acts as the "database" that stores all the
users. Also, note ``User.groups`` is a list of "groups" that the user belongs
to.

Adding User Object as Request Member
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While not 100% necessary, it's quite nice to access the ``User`` object in a
pyramid request as ``request.user``. That, and it's quite easy to set up!

All that needs to be done is supply a "user finding" function to our
Configurator.

.. code-block:: python
    :caption: get_user for request.user in auth_app/model/auth.py

    from pyramid.security import unauthenticated_userid

    def get_user(request):
        userid = unauthenticated_userid(request)
        if userid is not None:
            for user in USERS:  # querying our mock DB
                if user.userid == userid:
                    return user
        else:
            return None

Then, in the Configurator...

.. code-block:: python
    :caption: adding request.user member in Configurator in auth_app/app_config.py

    from auth_app.model.auth import get_user

    def main(global_config, **settings):
        ...
        config.add_request_method(get_user, 'user', reify=True)
        ...
        return config.make_wsgi_app()


This makes the return value of ``get_user(request)`` (a ``User`` object if
authenticated, ``None`` otherwise, as defined in the fxn) available as the
request member ``request.user`` without having to retrieve it ourselves!


Group/Principle Callback
++++++++++++++++++++++++

``AuthTktAuthenticationPolicy`` requires a "callback" function that returns
all memberships that a user has. Groups/memberships/whatever will be matched to
permissions by the authorization policy. 

.. code-block:: python
    :caption: "group finder" function in auth_app/model/auth.py

    def groupfinder(userid, request):
        user = request.user  # remember, we set this up w/ ``get_user``?
        if user is not None:
            return user.groups
        else:
            return None

This callback is responsible for assigning the "memberships" that we defined as
part of the ``User`` object. It doesn't matter how it does it, as long as a
list of strings is returned (or ``None`` if there are no memberhips).

Pyramid requires that all Authentication policies have an Authorization policy
to match. So, before we add it to the configurator, we should define the
Authorization policy.


Authorization
-------------

This example uses ``pyramid.authorization.ACLAuthorizationPolicy`` to handle
authorization.

**ACL**: **Access Control List**

    A sequence of ACE tuples

**ACE**: **Access Control Entry**

    A single element in the ACL that's composed of 3 things:

    1. An Action (``Allow`` or ``Deny`` from ``pyramid.security``)

    2. A Principal (a string describing a user or group)

    3. A Permission (a string describing the granted permission)

To handle assigning permissions, the pyramid ``Configurator`` is given an
"AuthorizationFactory" to distribute permissions on requests based off of a
user's groups.

.. code-block:: python
    :caption: RootFactory in auth_app/security/factory.py

    from pyramid.security import Allow, Everyone, Authenticated

    class RootFactory(object):

        __acl__ = [
                (Allow, Authenticated, "view"),
                (Allow, "group:admin", "admin"),
                ]

        def __init__(self, request):
            self.request = request


This is a pretty simple ``RootFactory`` in that all permissions are statically
assigned. However, the AuthorizationFactories can manipulate as much as they
please to assign/determine the ``__acl__`` based off the request.

This RootFactory gives all authenticated users the permission ``"view"``, and
all users with ``group:admin`` the ``"admin"`` permission.


Adding Authorization & Authentication to the Configurator
---------------------------------------------------------

Now that the dependancies from the policies are defined, they can be added to
the ``Configurator``. 

.. code-block:: python
  :caption: adding Authorization & Authentication to auth_app/app_config.py
  :emphasize-lines: 14-24

    from pyramid.config import Configurator
    from pyramid.authentication import AuthTktAuthenticationPolicy
    from pyramid.authorization import ACLAuthorizationPolicy

    from auth_app.security.factory import RootFactory
    from auth_app.model.auth import get_user, groupfinder


    def main(global_config, **settings):
        config = Configurator(settings=settings)
        ...
        config.add_request_method(get_user, 'user', reify=True)

        authn_policy = AuthTktAuthenticationPolicy(
                "auth_secret",  # should come from .ini or config file
                callback=groupfinder,
                hashalg='sha512',
                )
        config.set_authentication_policy(authn_policy)

        authz_policy = ACLAuthorizationPolicy()
        config.set_authorization_policy(authz_policy)

        config.set_root_factory(RootFactory)
        ...
        return config.make_wsgi_app()


Login & Logout Views
--------------------

Now that the Authorization & Authentication policies are set up, some sort of
authentication & deauthentication views need to be set up.

These views are used to check Authentication & give the response a header to
remember the "Auth Ticket" that's assigned so they can be recognized down the
road.

.. code-block:: python
    :caption: login/logout views in auth_app/views/views.py
    :emphasize-lines: 17-18, 23-24

    from pyramid.view import view_config, forbidden_view_config
    from pyramid.httpexceptions import HTTPFound
    from pyramid.security import remember, forget

    from auth_app.model.auth import USERS  # the user "database"


    @view_config(route_name='login', renderer="auth_app:templates/login.mako")
    def login(request):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            for user in USERS:  # "querying" the database for the credentials
                username_match = user.username == username
                password_match = user.password == password
                if username_match is True and password_match is True:
                    headers = remember(request, user.userid)
                    raise HTTPFound(request.route_url('index'), headers=headers)
        return {}

    @view_config(route_name="logout")
    def logout(request):
        headers = forget(request)
        return HTTPFound(request.route_url('login'), headers=headers)


Take special notice of the ``remember`` and ``forget`` function calls, and that
``headers`` is being passed along the HTTP redirect. This is the app giving the
user a punched "Auth Ticket" that says "this user is Authenticated w/ this
userid". 

*This is how pyramid can tell if somebody is authenticated*, and is
what the groupfinder/userfinder functions defined earlier use to determine what
permissions the user has.


Adding Permissions To Views
---------------------------

Now that users can authenticate, views can be protected by permissions so that
only certain users/authenticated users can access certain pages.

Developers can create whatever permissions they want (remember they're just
strings in the ACL model)!

All one has to do to protect a view w/ a permission is to add the
``permission=`` kwarg to ``@view_config``!

.. code-block:: python
    :caption: adding permissions to views in auth_app/views/views.py
    :emphasize-lines: 3

    @view_config(route_name="index",
            renderer="auth_app:templates/index.mako",
            permission="view",
            )
    def index(request):
        return {}

This protects the ``index`` view callable with the ``"view"`` permission. Any
users that have principals that match an ACE entry in ``RootFactory.__acl__`` that assings the ``"view"`` permission will be able to access this page, while anybody else will be served an HTTP 403 Forbidden error.

A 403 Forbidden View Callable
-----------------------------

Now that auth_app can serve 403 HTTP errors, it might be a good idea to define
a custom "forbidden view callable".

.. code-block:: python
    :caption: forbidden view callable in auth_app/views/views.py
    :emphasize-lines: 3

    from pyramid.view import forbidden_view_config

    @forbidden_view_config(renderer="auth_app:templates/forbidden.mako")
    def forbidden(request):
        return {}

Now when an app user gets a 403, they'll be served the ``forbidden(request)``
view callable!


Summary
-------


