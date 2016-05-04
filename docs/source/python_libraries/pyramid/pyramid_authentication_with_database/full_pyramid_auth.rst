.. _pyramid_full_auth:

=================================================================
Pyramid Auth w/ User Model, Hybrid Traversal, & Resource Matching
=================================================================

Building on top of the Authentication & Authorization basic example, this example goes into depth on how to practically use Auth w/ an accompanying model.


This example will cover the following:

1. Creating a User/Group model & Database
   1. Storing hashed user passwords
   2. Using sqlalchemys ``@hybrid_property``
2. Hybrid Traversal (instead of Route Matching or Traversal)
   1. Factories & resource matching
   2. ``request.context`` & it's relationship to factories & ``__acl__``
   3. ``request.route_url()`` referencing traversals


.. note::

   Look...

   I don't feel like explaining what one does and doesn't need to know to understand this example.

   Some of the integral pieces that hold this app together but don't quite fit the example topic are going to either be glossed over, or skipped altogether.

   Proceed with caution!


Setting Up a User Model
-----------------------

Since the goal of this application is authentication, the model is going to have to store passwords. It would be remiss to store these in plaintext in the database, so they're going to have to be hashed.

.. code-block:: python


    from hashlib import sha1
    import os

    from sqlalchemy import Column, Unicode, Integer
    from sqlalchemy.ext.hybird import hybrid_property

    from full_auth_app.model import Base


    class User(Base):
        __tablename__ = "user"

        id = Column(Integer, autoincrement=True, primary_key=True)
        username = Column(Unicode(32), unique=True)
        _password = Column('password', Unicode(255))  # @property = .password

        @hybrid_property
        def password(self):
            return self._password

        @password.setter
        def set_password(self, password):
            salt = sha1(os.urandom(60))
            salted_pwd = password + salt.hexdigest()
            sha1_hash = sha1(salted_pwd.encode("UTF-8"))
            self._password = salt.hexdigest() + sha1_hash.hexdigest()

        def validate(self, password):
            combined_password = password + self.password[:40]
            hashed_password = sha1(combined_password.encode("UTF-8"))
            passwords_match = self.password[40:] == hashed_password.hexdigest()
            return passwords_match


There's a few interesting things going on here. 

First off, ``User._password`` is the actual sqlalchemy ``Column`` object, while ``User.password`` is decorated with ``@hybrid_property``. Effectively, this allows the wrapping of the password attribute just like with the ``@property`` decorator in normal class definitions.

After ``User.password`` is defined as a ``@hybrid_property`` it behaves very similarly to a standard property allowing ``User.set_password`` to be wrapped with ``@password.setter`` to create a setter function for the property.

Lastly, ``User.validate(self, password)`` is the function that is used to validate a submitted password against a hashed password. It returns ``True`` if the arg ``password`` matches the hashed ``User._password``.

.. note::
   ``User.set_password`` assumes that the password supplied is UTF-8 already.

   Since hashing requires a ``bytes`` object, decoding/encoding & exception handling may be necessary.


Now that a sqlalchemy user model is set up, the "groupfinder" function (the *callback* arg supplied to ``AuthTktAuthenticationPolicy`` used to find the effective permissions) and the ``get_user`` fxn (used for ``request.user``) needs to be changed to reflect the new user model.

.. code-block:: python

    def get_user(request):
        """
        request.user - config.add_request_method(get_user, 'user', reify=True)
        """
        userid = unauthenticated_userid(request)
        user = Session.query(User).filter_by(id=userid).first()
        return user  # either a found User ORM object or None


    def groupfinder(userid, request):
        """
        AuthTktAuthenticationPolicy(..., callback=groupfinder, ...)

        relies on request.user from ``get_user(request)``
        """
        if request.user is not None:
            perms = list()
            perms.append("user:{}".format(request.user.username))
            # FIND ADDITIONAL PERMISSIONS HERE
            return perms
        else:
            return None

Since there are currently other permissions modeled (e.g. "Groups") the only permission that can be found is ``"user:<username>"``.

Hybrid Traversal & Resource Matching
------------------------------------

With a dynamic model set up for permissions, the need for dynamic permission declaration has arised.

A static set of permissions can't be used to reference a dynamic set of permissions.

To achieve this, an ``__acl__`` property can be assigned to an object, and then a "Factory" can retrieve this object as *context* for a routes request.

This is achieved using *Traversal* (pre-defining all routes & views during app configuration), which is the alternative to *URL Dispatch* (defining the routes by name in app config and scanning to match them to view callables). 

To leverage traversal while using URL Dispatch, views can be defined using *Hybrid Traversal* which is elaborated in depth in `the pyramid "Hybrid Traversal" doc <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hybrid.html#combining-traversal-and-url-dispatch>`__.

To start, let's define a "user_profile" route in ``app_config``

.. code-block:: python

    from pyramid.config import Configurator

    from full_auth_app.security.factory import RootFactory, UserFactory


    def main(global_config, **settings):
        config = Configurator(settings=settings)
        config.set_root_factory(RootFactory)
        ...
        config.add_route(
                name="user_profile",
                pattern="/user/{user_id}",
                factory=UserFactory,
                traverse="/{user_id}"
                )
        ...
        return config.make_wsgi_app()

This new "user_profile" route, instead of using the default ``RootFactory`` to determine permissions, uses ``UserFactory``.

Alongside this, using the *traversal* policy supplied by ``pattern="/user/{user_id}"`` and ``traverse="/{user_id}"``, a value supplied by the url is passed to ``UserFactory.__getitem__(self, user_id)`` and, if available, a ``User`` object is returned and set as ``request.context`` (else ``None``). 

This is effectively *Hybrid Traversal*: the routes are defined by names in configuration, but they're still being matched to view_callables using ``pyramid.view.view_config`` & are discovered w/ ``config.scan()``.



Defining Resource Factories & Context
+++++++++++++++++++++++++++++++++++++

Below is the code in ``security/factory.py`` that accomplishes resource matching.

.. code-block:: python

    from pyramid.security import Allow, Everyone, Authenticated

    from full_auth_app.model.auth import get_user


    class UserFactory(object):
        __acl__ = [
                (Allow, Authenticated, "view"),
                ]

        def __init__(self, request):
            self.request = request

        def __getitem__(self, user_id):
            user = get_user(id=user_id)
            if user is not None:
                return user
            else:
                return None

Since a ``request.context`` object is being supplied, it can also be used to provide permissions via ``__acl__``. Lets edit the ``User`` model to add this.

.. code-block:: python

    from pyramid.security import Allow, Deny, Everyone

    from full_auth_app.model import Base


    class User(Base):
        __tablename__ = "user"

        @property
        def __acl__(self):
            perms = list()
            perms.append((Allow, "user:{}".format(self.username), "edit"))
            return perms

        ...


Traversal, Resource Factories, & Context Explained
++++++++++++++++++++++++++++++++++++++++++++++++++

In the above example, the ``User.__acl__`` supplies an ``"edit"`` permission to anybody with the principal ``"user:<username>"``, which effectively means that only a user may edit themselves.

But one will notice that ``UserFactory`` & ``User`` both provide a set of ``__acl__``. These interact in a special way:

1. ``RootFactory`` is called before ANY other resources are generated. *All permissions from*  ``RootFactory.__acl__`` are factored in.
2. Traversal matches the route's resource locator to ``UserFactory``, which then *appends* ``UserFactory.__acl__`` to the __acl__'s collected from ``RootFactory``.
3. Traversal uses ``UserFactory.__getitem__`` to retrieve a ``User`` object. If one is found, ``User.__acl__`` *is then added to the collected* __acl__ objects.

Effectively, this works as a long parent-child tree of __acl__ objects. *ALL* views recieve the permissions determined from ``RootFactory``. Any views that use the resource ``UserFactory``, *even if* ``RootFactory.__getitem__`` *is not called* is given permissions from ``UserFactory``. Lastly, if any ``request.context`` object (returned from a resource like ``UserFactory.__getitem__`` during traversal) has an ``.__acl__`` property, those permissions are added.

In this example, traversal is only matching one resource locator and one context object, but it can become much more complex! Multiple levels of resources and resource locators can be called as they're traversed & matched. For a very in-depth view at how traversal works view `the official "Traversal Algorithm" from pyramid's docs <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/traversal.html#the-traversal-algorithm>`__.

Incorperating Context into a View Callable
++++++++++++++++++++++++++++++++++++++++++

Now that ``request.context`` can provide a ``User`` object specified by user_id in the URL, we can finish implementing the "user_profile" view this example set out to create.

.. code-block:: python

    from pyramid.view import view_config

    @view_config(route_name="user_profile", renderer="user_profile.mako",
            permission="view")
    def user_profile(request):
        return {"user": request.context}

It's that easy! Offloading the duty of matching the URL to a user & getting the permissions for that User's page to *resource matching* clears up the code for the view callable to be clean & efficient!
