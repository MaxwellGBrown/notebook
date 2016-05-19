.. _context: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-context  

.. _routes: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-route

.. _resource: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource

.. _resource tree: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource-tree

---------
Traversal
---------

Traversal is a routing system that is built around a model called the `resource tree`_. 

URLs are matched to views based off of the path segments provided in the request, which are used to navigate the resource tree until a `context`_ `resource`_ is found. That resource (now known as context), along with any left over path segments, is used to lookup a view callable, which then serves the response.

With Traversal, it's **required** that the ``Configurator`` is supplied a "Root Factory" which is the very first item in the resource tree that all items derive their lineage from.

Since the model/resource tree is so integral to a Traversal application's structure, it's easiest to start by defining what a resource is.


+++++++++++++++++
The Resource Tree
+++++++++++++++++

`The Resource Tree <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/traversal.html#the-resource-tree>`__ is the backbone of a Traversal application. While URL Dispatch applications are dependent on the *routes* defined in the application, Traversal Applications are defined by the *resource tree*, and are dependent on it's structure.

The Resource Tree is a heirarchy of `resources <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html>`__ that begin at a single RootFactory established by the ``Configurator``.

Resources are defined by their ``__name__`` attribute, which is responsible for their location & discovery, and their ``__parent__`` attribute which is the parent object responsible for serving them based on their ``__name__``.

Resources are considered `location-aware <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#location-aware>`__ if they have both their ``__name__`` and ``__parent__`` attributes defined (and the heirarchy of parents are also location aware).

When using Traversal, **all resources must be location aware**, meaning *every* resource must have it's ``__name__`` and ``__parent__`` defined.

~~~~~~~~
Resource
~~~~~~~~

  Any object with ``__parent__`` and ``__name__`` attributes.

  ``__parent__``

    The object that is the parent resource of *this* resource.
   
    Is ``None`` for the root factory.


  ``__name__``

    The key/id of *this* resource.
   
    Resource objects of the same class w/ equal ``__name__`` **must always** be equal. 
    
    Is ``None`` for the root factory.

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

  A resource that *does not* have ``__getitem__(self, key)`` defined, or is defined such that ``KeyError`` is always raised. 
  
  Represents the end of the resource tree (hence the name *leaf*).

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

  The very first resource in the resource tree, that has ``__name__ = None  # or ""`` and ``__parent__ = None``. 
  
  Is initialized by a request object ``__init__(self, request)`` and acts as a container resource to the next level of the resource tree.

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

   The RootFactory is initialized w/ a ``Request`` object, which seems significant.

   However, it's not required or suggested anywhere in pyramid docs to pass the request object through the resource tree.

   How does a 1st level resource reference the RootFactory (e.g. by creating one) if it doesn't have access to the request object?


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

**resource location** is the act of traversing the resource tree.

Resource location operates using the `traversal algorithm <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/traversal.html#the-traversal-algorithm>`__ which leverages the structure of the resource tree against the path to locate resources.

~~~~~~~~~~~~~~~~~~~~~~~
The Traversal Algorithm
~~~~~~~~~~~~~~~~~~~~~~~

1. Initialize the RootFactory with the request object. 

::

    context = RootFactory(request)  # __init__ if object or __call__ if fxn/already initialized

2. Use the 1st path segment as an argument to ``context.__getitem__(key)``

::

    # path: /foo
    context = context["foo"]  # RootFactory(request)['foo']

3. This is repeated with each new resource & path segment until...

   * the path segments have been exhausted
   * a leaf-resource is reached (does not have ``__getitem__`` defined)
   * a ``KeyError`` is raised.

The resulting object is then used as ``request.context`` and, if the view accepts it, the ``context`` \*arg for a matching view callable.

When played out fully, the traversal algorithm looks a lot like this:

::

  # path: /foo/bar/baz/qux

  request.context = RootFactory(request)['foo']['bar']['baz']['qux']

If this is unchained, it looks a lot like this:

::

  # path: /foo/bar/baz/qux

  request.context = RootFactory(request)
  request.context = request.context['foo']  # RootFactory['foo']
  request.context = request.context['bar']  # Foo['bar']
  request.context = request.context['baz']  # Bar['baz']
  request.context = request.context['qux']  # Baz['qux']

There's actually much more going on (like checking for ``__getitem__`` & handling ``KeyError``), but this demonstration highlights how resource location operates.


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




