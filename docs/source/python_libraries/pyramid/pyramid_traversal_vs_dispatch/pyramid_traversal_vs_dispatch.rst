
.. _context: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-context  

.. _routes: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-route

.. _resource: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource

.. _resource tree: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource-tree

==========================
Traversal vs. URL Dispatch
==========================

**Resources**

* `Much Ado About Traversal <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/muchadoabouttraversal.html>`__
* `Hybrid Traversal/URL Dispatch Factories <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#using-pyramid-security-with-url-dispatch>`__
* `*traverse in a Route Definition <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hybrid.html#using-traverse-in-a-route-pattern>`__


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

---------------------------
Which Should I Use and Why?
---------------------------

So now that the three different types of pyramid pathing are laid out, it's time to make a decision:

**Which type is most appropriate for my application?**

This section aims to break that down!

+++++++++++++++++++++++++++++++
When Should I Use URL Dispatch?
+++++++++++++++++++++++++++++++

**Most Always**

..
  URL Dispatch is the baby of ``pylons``.
  # Is this even true? Or did I make this up?

URL Dispatch is the most straightforward and explicit pathing scheme. With URL Dispatch it's very easy to tell which routes exist, which views match up to those routes, and what resources/contexts are being supplied to those views.

Additionally, though URL Dispatch might not get to crawl a bunch of resources to ensure the integrity of a model, it can provide the necessary resource/context in a very straightforward manor using the RouteFactory and matchdict to run one or two targeted queries.

~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reasons To Use URL Dispatch
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Application is more static than dynamic
* Views are typically small and model-independent
* Views aren less sensitive on model hierarchy, or only worry about the object they have 
* Permissions aren't nested or complex (dynamic is okay)
* User-generated content is defined by the application

++++++++++++++++++++++++++++
When Should I Use Traversal?
++++++++++++++++++++++++++++

**Usually Never**

..
  Traversal is the baby of ``repoze.bfg``.
  # Is this even true? Or did I make this up?

Traversal applications are defined by and are completely dependent on the resource tree of the application. This obfuscates a lot of things that are very transparent in URL Dispatch like the URLs/paths for specific pages or routing to specific views.

That being said, Traversal's defining feature is the reason why you would use it: *application structure is tied to the resource tree*. This means that applications that rely on a complex model can likely be served better served as a Traversal application. This way, instead of defining routes & views that work alongside the model, the model can define the routes and the views can be integrated as needed.

~~~~~~~~~~~~~~~~~~~~~~~~
Reasons To Use Traversal
~~~~~~~~~~~~~~~~~~~~~~~~

* Application & routing is highly dependent on the model
* Views and templates are less context-sensitive (doesn't care what context you give it)
* Model exists before application, & application is highly-dependent on model
* User-generated content is defined by the model
* Application content is reliant on complex user-generated content model

+++++++++++++++++++++++++++++++++++
When Should I Use Hybrid Traversal?
+++++++++++++++++++++++++++++++++++

**When you need to**

Hybrid Traversal, being a combination of both structures, should be used when your application desires functionality from the other method.

Unless you know from the initialization of the project that you'll need Hybrid Traversal, start with either URL Dispatch or Traversal. Develop the application using said method until you reach a point where you want to leverage a feature from the other method.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reasons To Use Hybrid Traversal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Application was developed with URL Dispatch but wants to leverage Traversal for one or more routes.
* Application was developed with Traversal but wants routes defined for different resource trees, more staticly defined routes, etc.



------------------
A Quick Comparison
------------------

Below is a breakdown of URL Dispatch vs Traversal in table form

================================ ====================================== =============================================================
How does it handle...            URL Dispatch                           Traversal                                                     
================================ ====================================== =============================================================
App Configuration                Routes added to ``Configurator``       RootFactory for resource tree defined in ``Configurator``
Matching views to request urls   path matches route_name's pattern      leaf-resource & view_name match a view callable's view_config
View Configuration               ``@view_config(route_name="")``        ``@view_config(name="", context=ResourceCls)``
View \*args                      ``view(request):``                     ``view(context, request):`` *or* ``view(request):``
Generating URLs                  ``request.route_url("")``              ``request.resource_url(resource, "view_name")``
Route Factories                  Per-route, w/ RootFactory default      All part of one large resource tree, starting w/ RootFactory
Resource Tree                    ``request.matchdict`` to get context   ``context = resource.__getitem__(key)`` recursively 
Resources/context                Location un-aware                      **Must** be location aware (``__name__`` & ``__parent__``)
================================ ====================================== =============================================================

Notice that *URL Dispatch relies more on the applications structure* while *Traversal is more dependent on the resource tree's structure*.



------------
URL Dispatch
------------

`URL Dispatch <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#urldispatch-chapter>`__ relies on defining more static `routes`_ which have it's values
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
    /1/2/3/  => HTTPNotFound # (trailing slash)
    /1/2/3/4 => HTTPNotFound # (no route for 4th element)

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


+++++++++++++++++++++
Prefixing Route Paths
+++++++++++++++++++++

Having statically defined routes allows one to prefix routes quite easily. 

.. code-block:: python

    from pyramid.config import Configurator

    def main(global_config, **settings):
        config = Configurator()

        def user_views(config):
            config.add_route('show_users', '/show')

        def group_views(config):
            config.add_route('show_groups', '/show')
            config.include(user_views, route_prefix='/users')

        config.include(user_views, route_prefix='/groups')

        return config.make_wsgi_app()

Using this nested structure for adding route prefixes, the generated routes look something like this:

::

  request.route_path('show_groups')
  >>> /groups/show

  request.route_path('show_users')
  >>> /groups/users/show



.. _url_dispatch_resource_location:

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


+++++++++++++++++++++++
Custom Route Predicates
+++++++++++++++++++++++

When using matchdict to handle URL & path matching, it's sometimes good to define custom predicates to better handle URL translation.

`Custom Route Predicates <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#custom-route-predicates>`__ let one define exactly what in the route is being handled.

.. code-block:: python

   def integer_predicate(segment_name):
       def _integer_predicate(info, request):  # THIS is the custom predicate
           if info['match'][segment_name].isdigit():
               return True  # return True if success, return None/False if fail
       return _integer_predicate

   config.add_route('route_to_num', '/{num}', custom_predicates=(integer_predicate('num'),))
            
The above example performs just checking of the URL, but predicates can also be used to convert the values supplied by matchdict.

.. code-block:: python

    def as_int_predicate(segment_name):
        def _as_int_predicate(info, request):  # THIS is the custom predicate
            try:
                match[segment_name] = int(match[segment_name])
            except (TypeError, ValueError):
                pass
            return True  # type conversion predicates should always return True if successful
        return _as_int_predicate

    config.add_route('route_to_num', '/{num}', custom_predicates=(as_int_predicate('num'),))

Using custom predicates, you can supply some interesting values to ResourceFactories w/ URL Dispatch.

---------
Traversal
---------

Traversal is a routing system that is built around a model called the `resource tree`_. 

URLs are matched to views based off of the path segments provided in the request, which are used to navigate the resource tree until a `context`_ `resource`_ is found. That resource (now known as context), along with any left over path segments, is used to lookup a view callable, which then serves the response.

With Traversal, it's **required** that the ``Configurator`` is supplied a "Root Factory" which is the very first item in the resource tree that all items derive their lineage from.

Since the model/resource tree is so integral to a Traversal application's , it's easiest to start by defining what a resource is.


+++++++++++++++++
The Resource Tree
+++++++++++++++++

`The Resource Tree <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/traversal.html#the-resource-tree>`__ is the backbone of a Traversal application. While URL Dispatch applications are dependent on the routes defined in the application, Traversal Applications are defined by the resource tree, and are dependent on it's structure.

The Resource Tree is a heirarchy of `resources <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html>`__ that begin at a single RootFactory. Resources are defined by their ``__name__`` attribute, which is responsible for their location & discovery, and their ``__parent__`` attribute which is the parent object responsible for serving them based on their ``__name__``.

~~~~~~~~
Resource
~~~~~~~~

  Any object with the ``__parent__`` and ``__name__`` attributes.

  ``__parent__``

    The parent resource of the resource. Is ``None`` for the root factory.


  ``__name__``

    The key/id of this resource. Resource objects of the same class w/ equal ``__name__`` **must always** be equal. Is ``None`` for the root factory.

That's all that's required to define a Resource!

.. code-block:: python
    :emphasize-lines: 3,4

    class Resource(object):  # a resource w/ minimum requirements
        def __init__(self, parent, name):
            self.__parent__ = parent
            self.__name__ = name


Now that a standard `resource`_ is defined, there are two sub-types of resources with important distinctions:

~~~~~~~~~~~~~~~~~~
Container Resource
~~~~~~~~~~~~~~~~~~

  A dict-like resource (has ``__getitem__(self, key)`` defined) that, when supplied a key, will return the next resource in the resource tree identified by that key.

  ``__getitem__(self, key)``

    Returns the next resource in the resource tree where ``__name__ == key`` and ``__parent__ is self`` (``self`` being the object called w/ ``__getitem__``)

    If no resource with ``__name__ == key`` can be found, ``KeyError`` should be raised.

.. code-block:: python
    :emphasize-lines: 6,7

    class ContainerResource(object):
        def __init__(self, parent, name):
            self.__parent__ = parent
            self.__name__ = name

        def __getitem__(self, key):
            return Resource(parent=self, name=key)

Note that container resources can return other container resources, or can also raise key errors if that child with the supplied ``__name__`` can't be found.

~~~~~~~~~~~~~
Leaf Resource
~~~~~~~~~~~~~

  A resource that *does not* have ``__getitem__(self, key)`` defined, or is defined such that ``KeyError`` is always raised. Represents the end of the resource tree (hence the name *leaf*).

.. code-block:: python
    :emphasize-lines: 6,7

    class LeafResource(object):
        def __init__(self, parent, name):
            self.__parent__ = parent
            self.__name__ = name

        # def __getitem__(self, key):
        #     raise KeyError()



~~~~~~~~~~~~
Root Factory
~~~~~~~~~~~~

  The very first resource in the resource tree, that has ``__name__ = None  # or ""`` and ``__parent__ = None``. Is initialized by a request object ``__init__(self, request)`` and acts as a container resource to the next level of the resource tree.

.. code-block:: python
    :emphasize-lines: 2,3

    class RootFactory(object):
        __name__ = None  # or ""
        __parent__ = None
    
        def __init__(self, request):
            pass 

        def __getitem__(self, key):
            return ContainerResource(parent=self, name=key)

.. note::

   I'm not sure how important it is, but the request object seems like it should be passed down the chain. 

   This way, the ``__parent__`` property written above can pass the parent objects the request instead of ``None``, and that request can be manipulated appropriately.


~~~~~~~~~~~~~~~~~~~~~~~~~~~
sqlalchemy Resource Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's a quick example of what a resource tree might look like in sqlalchemy

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



++++++++++++++++++++++++++++++++++++++++++++++++++
Traversing The Resource Tree aka Resource Location
++++++++++++++++++++++++++++++++++++++++++++++++++

Traversal uses the resource tree to find a resource to serve as `context`_ for a request based on PATH_INFO (the tuple of path keys from the URL).

Traversal starts by initializing the RootFactory with the request object. 

Then, the \*args from PATH_INFO are used as keys for container resource's ``__getitem__`` to find the next resource in the resource tree. This is done with each new resource until all of the PATH_INFO \*args have been used, a leaf-resource is reached, or a ``KeyError`` is raised.

The resulting object is then used as ``request.context`` and, if the view accepts it, the ``context`` \*arg for a matching view callable.

The act of *traversing the resource tree* is called **resource location**.

The `Traversal/resource location algorithm <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/traversal.html#the-traversal-algorithm>`__ uses the structure of parents & names defined by the resource tree.

::

  # path: /foo/bar/baz/qux

  request.context = RootFactory(request)['foo']['bar']['baz']['qux']

The traversal algorithm, unchained, looks like this

::

  # path: /foo/bar/baz/qux

  request.context = RootFactory(request)
  request.context = request.context['foo']  # RootFactory['foo']
  request.context = request.context['bar']  # Foo['bar']
  request.context = request.context['baz']  # Bar['baz']
  request.context = request.context['qux']  # Baz['qux']


+++++++++++++++++++++++++++
View Callables in Traversal
+++++++++++++++++++++++++++

To match requests to view callables, Traversal performs a `view lookup <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/muchadoabouttraversal.html#view-lookup>`__.

After resource location, Traversal tries to match a view based on the ``request.context`` and the ``view_name``.

View name is determined as *the first path segment that is not used in resource location*.

The view lookup algorithm acts like this...

.. code-block:: python

    # path: /foo/bar/profile
    context = get_root(request)['foo']['bar']  # Bar['profile'] => KeyError
    request.context = context
    view_callable = get_view(context, "profile")  # the 1st unused PATH_INFO
    view_callable(request)  # or view_callable(context, request)

...with a few exceptions:

* If there's no view match for the context object a view with the same name but no context will be matched.
* If no view name is available from the path (no KeyError is raised & all of PATH_INFO was used) then an unnamed view with the same context will be matched.
* If neither of the above match, an unnamed view with no context will be matched.
* If no views match, an ``HTTPNotFound`` will be raised.

Below are some example paths that show what the view_name and resource are after resource location and view lookup.

::

  # resource tree: RootFactory => Foo => Bar

  /foo/bar/baz   => view_name: "baz",   context: Bar,                   
  /foo/bar/hello => view_name: "hello", context: Bar,                   
  /foo/bar       => view_name: "",      context: Bar,                   
  /foo/hello     => view_name: "",      context: Bar(__name__='hello'), 
  /hello         => view_name: "",      context: Foo(__name__='hello'), 


Defining views in traversal is easy: because view lookup is performed based on a view's ``@view_config`` there's no need to include them in the ``Configurator`` (if not using ``@view_config``, add them with ``Configurator.add_view()``.

A Traversal view only needs the necessary information needed to find it during view lookup. This means that it *should* supply ``context=ResourceClass`` to match the ``request.context`` to, or ``name="view_name"`` to match the view_name to.

.. code-block:: python

    # traversal_app/views.py
    @view_config()  # no name, no context; matches all unmatched in view lookup
    def default(request):  # def default(context, request)
        raise HTTPNotFound()

    @view_config(context=RootFactory)  # RootFactory context, no name. matches '/' path
    def index(request):  # def index(context, request)
        return Response("index")

    @view_config(name="hello", context=Resource)
    def hello(request):  # def hello(context, request)
        return Response(request.context.__name__)


    # traversal_app/app_config.py
    def main(global_config, **settings):
        config = Configurator(settings=settings)
        ...
        config.set_root_factory(RootFactory)
        # config.add_view("traversal_app.views.hello", name="hello", context=Resource)
        ...
        config.scan()
        return config.make_wsgi_app()


++++++++++++++++++++++++++++++++++++
Generating URLs & Paths in Traversal
++++++++++++++++++++++++++++++++++++

`Generating the URLs and paths of resources <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#generating-the-url-of-a-resource>`__ is dependent on their ``__name__`` and where they exist in the heirarchy of the resource tree.

Resource URLs & paths are generated using the resource object using ``request.resource_url()`` and ``request.resource_path()`` respectively.

Since Traversal does not use any routes to match view callables, a view_name (if desired) must be passed as an extra \*arg.


::

  request.resource_url(RootFactory)
  >>> http://host/

  request.resource_url(Bar)
  >>> http://host/foo/bar

  request.resource_url(Bar, 'hello')
  >>> http://host/foo/bar/hello

  request.resource_url(Bar, 'hello', 'world')
  >>> http://host/foo/bar/hello/world


++++++++++++++++++++++++
Containment & Interfaces
++++++++++++++++++++++++

.. note::
    While I haven't experimented with it yet, it seems like the ``containment`` view configuration `predicate argument <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/viewconfig.html#predicate-arguments>`__ and `interfaces <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#resources-which-implement-interfaces>`__ for resource objects could be a nice addition to Traversal Mastery



++++++++++++++++++++++++++++++++++++++++++
Troubleshooting Traversal & Best Practices
++++++++++++++++++++++++++++++++++++++++++

Here are some solutions to problems!

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Avoiding view_name & Resource.__name__ collisions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    I've answered `my stack overflow post <http://stackoverflow.com/questions/37218572/pyramid-traversal-name-matching-a-view-name>`__ about this issue, but there's still room for discussion on other solutions.

To avoid collisions of view_names and resource __name__s, it's a good idea to use a "dummy" container to separate container resources.


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


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Debugging Traversal View Lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To include extra information about context and view names in 404 Not Found responses, add the following to the ``.ini`` used to initialize the application.

::

  [app:main]
  ...
  pyramid.debug_notfound = true
  ...



----------------
Hybrid Traversal
----------------

Since neither Traversal or URL Dispatch is mutually exclusive (they can both coexist in the same application), different aspects of their pathing can be leveraged side-by-side or even work together.

`Hybrid Traversal <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hybrid.html>`__ is defined as any application that leverages any part of both URL Dispatch & Traversal.

In practice, Hybrid Traversal *is* a Traversal-based application, except:

* the traversal root is chosen based on the defined route instead of from the
  ``root_factory``
* the traversal path is chosen based on the route configuration instead of
  ``PATH_INFO``
* the set views to be chosen in view lookup are limited to those that match the
  route_name in their configuration.

In Hybrid Traversal, the traversal is performed during a request after a route
had maatched, instead of matching a route to a view based on the resource tree.

.. code-block:: python

    # URL Dispatch 
    config.add_route('foobar', '{foo}/{bar}')

    @view_config(route_name='foobar')
    def url_dispatch(request):
        return Response()


    # Traversal
    config.set_root_factory(ResourceTreeRoot)

    @view_config(name="foobar", context=ResourceClass)
    def traversal(context, request):
        return Response()


    # Hybrid
    config.add_route(
            route_name="foobar",
            factory=FooBarFactory,
            pattern="/foo/bar*traverse",
            traverse="*traverse",
    )

    @view_config(route_name="foobar", name="view", context=FooResource)
    def view_foo(context, request):
        return Response()


The most distinguishing difference between Traversal & URL Dispatch is pathing & view matching. The below examples will break into the hybridization of these.

++++++++++++++++++++++++++++++++++
Routes & Views in Hybrid Traversal
++++++++++++++++++++++++++++++++++

To reiterate, Hybrid Traversal is essentially a Traversal application with defined routes.

Hybrid Traversal routes act kind of as "isolated resource trees" in that you can supply them factories different than the root resource factory. Within that route, Traversal will operate just like it normally would, but only using the views attached to that route, and only traversing throught the resource tree starting with the supplied factory.

Below will break down how a traversal app uses routes along w/ traversal.

Each example will break down

1. The route configuration in the ``Configurator``
2. The ``@view_config`` for a view that works w/ that route
3. Generating a URL for the route

~~~~~~~~~~
route_name
~~~~~~~~~~

Revisiting the backbone of URL Dispatch, just a plain route defined by a route name.

.. code-block:: python

    # configurator
    config.add_route(route_name="basic_route", pattern="/basic")

    # view_config
    @view_config(route_name="basic_route")
    def basic(request):
        return Response()

    # URL generation
    request.route_url("route_name")


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
route_name & url path matching by Traversal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In the url pattern for routes, you can supply the ``traverse`` kwarg to handle how far down a URL matching pattern the root factory will traverse.

The ``traverse`` kwargs allows for tight control on what gets run through the resource tree, and what gets called by ``ResourceTree.__getitem__`` from the PATH_INFO.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A "Pure Traversal" Hybrid Traversal route
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a Hybrid Traversal route, in that it's a route. Otherwise, this route is completely defined by the traversal of the request PATH_INFO.

.. code-block:: python

    # Hybrid Traversal "pure traversal" Configurator route
    config.add_route(
            route_name="traversal_route",
            factory=FooBarFactory,
            pattern="/traversal/route*traversal",
            traverse="*traversal",  # this is actually redundant
            )

    # view_config for traversal hybrid traversal route. Works just like Traversal!
    @view_config(name="view", route_name="traversal_route", context=ResourceCls)
    def pure_traversal_view(context, request):
        return Response()

    # pure_traversal URL generation. Supply route_name along w/ traversal
    request.resource_url(resource, "view", route_name="traversal_route")
    # >>> http://host/traversal/route/resource/path/view

Again, this route operates like a traversal separate resource tree within the route. This includes views that are matched to requests by ``view_name`` matching the leftover PATH_INFO, and views that are matched by context class.

Leveraging this is how Traversal can best co-exist within a URL Dispatch application (thus becoming Hybrid).


^^^^^^^^^^^^^^^^^^^^^^^^^^
Matchdict Hybrid Traversal
^^^^^^^^^^^^^^^^^^^^^^^^^^

Like suggested w/ URL Dispatch & resource allocation, URL-match variables can be defined in the route pattern. If the ``traverse`` kwarg is supplied while adding the route, it will define the values supplied to the resource tree to determine ``request.context``.

.. code-block:: python

    # Configurator.add_route
    config.add_route(
            route_name="match_dict_traverse",
            factory=FooBarFactory,
            pattern="/match_dict_traverse/a/{b}/c/{d}",
            traverse="/a/{b}/c/{d}",
            # context = FooBarFactory(request)['a'][{b}]['c'][{d}]
    )

    # view_config for match_dict_traverse by route name
    @view_config(route_name="match_dict_traverse")
    def match_dict_trav_view(request):
        return Response()

    # URL Generation
    request.route_url("match_dict_traverse", b="B", d="D")
    # the resource_url can be generated in matchdict traversals, but the resources need
    # to be location-aware, meaning they need to handle the static portions of the path
    # (e.g. a & c in this example). This is probably not the best idea :)
    request.resource_url(ResourceD, "view_name", route_name="match_dict_traverse")


Doing this you can tightly control the arguments from the route pattern that are supplied to the ``__getitem__`` methods of the context. This is probably the "middle ground" between traversal and URL Dispatch, although there's arguably little benefit to using routes like this instead of `URL Dispatch resource location <url_dispatch_resource_location>`_.


^^^^^^^^^^^^^^^^^^^^^
Matchdict & Traversal
^^^^^^^^^^^^^^^^^^^^^

Sometimes static dividers for pathing are desired before traversing. 

Using matchdict to create the earlier portions of the URL before traversing at the end of the path allows for a specific resource tree to exist for that route after

.. code-block:: python

    # Configurator.add_route
    config.add_route(
            route_name="both",
            factory=FooBarFactory,
            pattern='/both/{foo}/bar*traverse',
            traverse="*traverse",
            # request.matchdict['foo'] = {foo}
            # FooBarFactory(request)[traverse1][traverse2]...
    )

    # view_config for matchdict & traverse
    @view_config(route_name="both", context=Resource)
    def both(request):
        return Response()

    # URL Generation
    request.resource_url(resource, route_name='both', route_kw={'foo': 'Hello'})


