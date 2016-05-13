
.. _routes: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-route

.. _resource: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource

.. _resource tree: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource-tree

==========================
Traversal vs. URL Dispatch
==========================

**Resources**

* `URL Dispatch <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#urldispatch-chapter>`__
* `Much Ado About Traversal <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/muchadoabouttraversal.html>`__
* `Resources <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html>`__
* `The Resource Tree <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/traversal.html#the-resource-tree>`__
* `Hybrid Traversal/URL Dispatch Factories <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#using-pyramid-security-with-url-dispatch>`__
* `*traverse in a Route Definition <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hybrid.html#using-traverse-in-a-route-pattern>`__
* `Traversal Linking to Views <http://stackoverflow.com/questions/15090863/how-to-generate-url-to-view-when-using-traversal>`__


Pyramid has two main methods to manage *mapping URLs to view callables*:

**URL Dispatch**

  Defining `routes`_ and their parameters to match URLs to view callables. Views are matched to routes & URLs by ``route_name``.

**Traversal**

  Defining location-aware `resources <resource>`_ which are linked together by a  `resource tree`_. Views are defined by name and matched by context and view name. The view callables manipulate the resource as ``request.context``


Traversal & URL Dispatch can be mixed to operate as a 3rd *URL mapping* method

**Hybrid Traversal**

  Defining *routes* (as in URL Dispatch) with match-keys/traversals that map directly to views, but leverage *resource lookup* (much like Traversal's *resource tree*) to match portions of the URL to a *resource* object which is passed to the view callable as ``request.context``. 
  
  However, Hybrid Traversal's resources are not `location-aware resources <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#location-aware>`__ as the *resource tree* isn't walked to locate the *resource*.


A pyramid application isn't bound to using just one of these 3 mapping patterns; Traversal, URL Dispatch, & Hybrid Traversal can all exist within the same application!

------------------
A Quick Comparison
------------------

Below is a breakdown of URL Dispatch vs Traversal in table form

================================ =================================== ============================================================
How does it handle...            URL Dispatch                        Traversal                                                    
================================ =================================== ============================================================
Mapping URLs to view callables   ``@view_config(route_name="")``     ``@view_config(name="")``
Generating URLs                  ``request.route_url("")``           ``request.resource_url(resource, "view_name")``
Adding views to the Configurator ``config.add_route(route_name="")`` leaf-resource & view_name match or ``config.add_view()``
Route Factories                  Per-route, w/ RootFactory default   All part of one large resource tree, starting w/ RootFactory
Resources/context                Location un-aware                   **Must** be location aware (``__name__`` & ``__parent__``)
================================ =================================== ============================================================


------------
URL Dispatch
------------

URL Dispatch relies on defining more static `routes`_ which have it's values
decoded in a URL as ``request.matchdict``, a key-value of the routes to their
URL pattern.

.. code-block:: python

    from pyramid.config import Configurator


    def main(global_config, **settings):
        config = Configurator(settings=settings)
        ...
        config.add_route('foo', pattern='/{foo}')
        config.add_route('bar', pattern='/{foo}/{bar}')
        config.add_route('baz', pattern='/{foo}/{bar}/{baz}')
        ...
        config.scan()
        return config.make_wsgi_app()

In the above example, 3 routes are defined, and each of them include another
"nested" value to match in the URL.

Below are what the URLs & their matchdicts would look like::

    # URL    => request.matchdict
    /1       => {"foo": "1"} 
    /1/2     => {"foo": "1", "bar": "2"}
    /1/2/3   => {"foo": "1", "bar": "2", "baz": "3"}
    /1/2/3/  => 404 HTTPNotFound (trailing slash)
    /1/2/3/4 => 404 HTTPNotFound (no route for 4th element)

Pyramid's docs has an in-depth breakdown of `URL Dispatch's Route Pattern Syntax <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#route-pattern-syntax>`__.


+++++++++++++++++++++++++++++++
Generating URLS w/ URL Dispatch
+++++++++++++++++++++++++++++++

Again, URLs in URL Dispatch are mapped by the defined `routes`_. Since this is
the case, `request.route_url <http://docs.pylonsproject.org/projects/pyramid/en/latest/api/request.html#pyramid.request.Request.route_url>`__
is the primary method of generating URLs within the application.

::

  request.route_url('foo', foo=1)        => http://localhost/dispatch_app/1
  request.route_url('bar', foo=1, bar=2) => http://localhost/dispatch_app/1/2

This should be pretty familiar, as this is the basic URL generation for simple
pyramid routes. However, it's worth reviewing because *traversal does things
differently*.

+++++++++++++++++++++++++++++++++++++++++
Route Factories & Context w/ URL Dispatch
+++++++++++++++++++++++++++++++++++++++++

Referencing the ``request.matchdict`` inside view callables or templates is
pretty easy and straightforward, but it pushes a bunch of things outside of the
applicaiton's management into the views management. 

For example, if the view in question is pulling up a "user profile", the view
is responsible for

1. Retrieving the "user profile" model object based on ``request.matchdict``.
2. Handling what happens if the "user profile" model can't be found based on
   the values in ``request.matchdict``
3. Checking the requester's permissions against the "user profile" model
   object.

This is where Route Factories & Context objects trickle down from Traversal.

Typically, a route factory is leveraged by initializing it with a ``request`` object and then climbing the resource tree using ``__getitem__`` from each resource.

::

  # /{foo}/{bar}/{baz}
  request.context = RouteFactory(request)[foo][bar][baz]

However, if no ``__getitem__`` method is defined by the factory, the object
returned from the route factory will be defined as the context.

.. code-block:: python

  def baz_factory(request):
      """
      Leverage request.matchdict to return an object for request.context

      This would typically return some sort of database model
      """
      class ContextObj(object):
          __acl__ = []
          def __init__(self, **kwargs):
              for k, v in kwargs.items():
                  setattr(self, k, v)

      return ContextObj(**request.matchdict)

  # app_config:main()
  def main(global_config, **settings):
      ...
      config.add_route("baz", pattern="/{foo}/{bar}/{baz}", factory=baz_factory)
      ...
      return config.make_wsgi_app()


Again, by defining a 1-step route factory (``baz-factory``) & leveraging ``request.matchdict``, a ``request.context`` object can be returned and used in the view callable, instead of the view callable finding & creating this object.

Also, this allows for additional ``__acl__`` permissions to be attached to the
context object being returned, so that the permissions defined in
``@view_config`` are matched against ``request.context`` before the view is
even called!


---------
Traversal
---------

Traversal uses the `resource tree`_ to match URLs to view callables.

The `resource tree`_ is a tree that starts w/ a root *route factory* and branches from there to other `resource`_ objects. The resources are traversed by requesting the next `resource`_ in the `resource tree`_ until either the URL keys are depleted, or a *leaf*-resource has been reached. 

Since the model/`resource tree`_ is so integral to Traversal pathing, it's easiest to start by defining the resource/model objects


+++++++++++++++++
The Resource Tree
+++++++++++++++++

Before talking about the different types of resources it's important to understand *what* a resource is:

**resource**

  Any object with the ``__parent__`` and ``__name__`` attributes.

  ``__parent__``

    The parent resource of the resource. Is ``None`` for the root factory.


  ``__name__``

    The key/id of this resource. Resource objects of the same class w/ equal ``__name__`` **must always** be equal. Is ``None`` for the root factory.


Now that a standard `resource`_ is defined, there are two sub-types of resources with important distinctions:


**container resource**

  A dict-like resource (has ``__getitem__(self, key)`` defined) that, when supplied a key, will return the next resource in the resource tree identified by that key.

  ``__getitem__(self, key)``

    Returns the next resource in the resource tree where ``__name__ == key`` and ``__parent__ is self`` (``self`` being the object called w/ ``__getitem__``)

    If no resource with ``__name__ == key`` can be found, ``KeyError`` should be raised.


**leaf resource**

  A resource that *does not* have ``__getitem__(self, key)`` defined, or is defined such that ``KeyError`` is always raised. Represents the end of the resource tree (hence the name *leaf*).


While the concept of the resource tree seems somewhat convoluted in writing, it's straightforward in practice.

Traversing the resource tree is called *resource location*, and it's used to determine the ``request.context``.

Shown below is a breakdown of what's happening in *resource location*:

::

  # path: /foo/bar/baz/qux

  request.context = RootFactory(request)['foo']['bar']['baz']['qux']

When broken apart, it looks like this

::

  # path: /foo/bar/baz/qux

  request.context = RootFactory(request)
  request.context = request.context['foo']  # RootFactory['foo']
  request.context = request.context['bar']  # Foo['bar']
  request.context = request.context['baz']  # Bar['baz']
  request.context = request.context['qux']  # Baz['qux']


*Resource location* will continue until one of two things happen:

1. A leaf resource is located

2. All path segments in the URL have been handled

Below is an example of a ``sqlalchemy`` ORM object & a factory that might appera in a resource tree:

.. code-block:: python

    class RootFactory(object):
        __name__ = None
        __parent__ = None

        def __init__(self, request):
            self.request = request

        def __getitem__(self, key):
            try:
                return Session.query(Resource).filter_by(name=key).one()
            except:
                raise KeyError

    class Resource(Base):

        @property
        def __name__(self):
            return self.name

        @property
        def __parent__(self):
            return RootFactory(None)

        __tablename__ = 'resource'

        name = Column(Unicode(100), primary_key=True)

.. note::

   I'm not sure how important it is, but the request object seems like it should be passed down the chain. 

   This way, the ``__parent__`` property written above can pass the parent objects the request instead of ``None``, and that request can be manipulated appropriately.


~~~~~~~~~~~~~~~~~~~~~~~~~
Dummy Container Resources
~~~~~~~~~~~~~~~~~~~~~~~~~

With the above set up, all Resource objects begin their inheritance from ``RootFactory`` and will inherit from other Resources, causeing the URL to always be the chain of Resource inheritance.

If one wanted to manipulate URLs tighter in Traversal, they could create a "dummy" container resource.


.. code-block:: python
    :emphasize-lines: 8-12,15,21-25,35

    class RootFactory(object):
        __name__ = None
        __parent__ = None

        def __init__(self, request):
            self.request = request

        def __getitem__(self, key):
            if key == "resource":
                return ResourceFactory(self)
            else:
                raise KeyError

    class ResourceFactory(object):
        __name__ = "resource"

        def __init__(self, parent)
            self.request = request
            self.__parent__ = parent

        def __getitem__(self, key):
            try:
                return Session.query(Resource).filter_by(name=key).one()
            except:
                raise KeyError

    class Resource(Base):

        @property
        def __name__(self):
            return self.name

        @property
        def __parent__(self):
            return ResourceFactory(RootFactory(None))

        __tablename__ = 'resource'

        name = Column(Unicode(100), primary_key=True)


Using ``ResourceFactory`` and having ``RootFactory`` act as it's parent, now resource paths like ``/resource/foo`` can be generated instead of ``/foo``.


+++++++++++++++++++++++++++
View Callables in Traversal
+++++++++++++++++++++++++++

In Traversal, views are configured to match a ``name`` (view name) and a ``context`` instead of a ``route_name``. This is called `view lookup <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/muchadoabouttraversal.html#view-lookup>`__.

After traversing the resource tree based on the URL, pyramid will match a view callable to the request based on the class of ``request.context`` and the leftover pieces of the URL not used in resource matching.

.. code-block:: python

    # traversal_app/views.py
    @view_config(name="hello", context=Resource)
    # def hello(context, request):  # optional, since request.context = context
    def hello(request):
        return Response(request.context.__name__)


    # traversal_app/app_config.py
    def main(global_config, **settings):
        config = Configurator(settings=settings)
        ...
        # optionally, instead of @view_config
        # config.add_view("traversal_app.views.hello", name="hello")
        config.set_root_factory(RootFactory)
        ...
        config.scan()
        return config.make_wsgi_app()


Notice how there's no definition of how URLs are supposed to match the view, etc. That's becausse the URL will do a traversal until it reaches a leaf-resource.

Also, in a Traversal **all traversing must start at the same root factory**, meaning that ``config.set_root_factory()`` is important because it's the very start of the resource tree.

If there is a portion of the URL path leftover, a view name can be matched to that leftover pathing, AND the ``request.context`` is of the class supplied in ``@view_config(context=)``, that view will be called.

::

  # RootFactory => Foo => Bar

  /foo/bar/hello => context: Bar, view: "hello"
  /foo/bar => context: Bar, view_name: ""
  /foo/hello => context: Bar(__name__='hello'), view_name: ""
  /hello => context: Foo(__name__='hello'), view_name: ""


.. note::

   Still not sure what to do about collisions where a resource ``__name__`` matches a view name.

   `I have an open stack overflow post about it <http://stackoverflow.com/questions/37218572/pyramid-traversal-name-matching-a-view-name>`__


Because there are no routes in Traversal, URL generation are handled by resources ``__name__`` and climbing theirs ``__parents__``. 

::

  request.resource_url(resource, 'hello')
  >>> http://localhost/foo/bar/hello
  request.resource_path(resource, 'hello', 'world')
  >>> /foo/bar/hello/world

This idea is covered `in pyramid's resources docs <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#generating-the-url-of-a-resource>`__.



++++++++++++++++++++++++
Containment & Interfaces
++++++++++++++++++++++++

.. note::
    While I haven't experimented with it yet, it seems like the ``containment`` view configuration `predicate argument <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html#predicate-arguments>`__ and `interfaces <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#resources-which-implement-interfaces>`__ for resource objects could be a nice addition to Traversal Mastery


----------------
Hybrid Traversal
----------------
