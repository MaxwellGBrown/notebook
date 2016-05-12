
.. _routes: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-route

.. _resource: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource

.. _resource_tree: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource-tree

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

  Defining `routes`_ and their parameters to match URLs to view callables.

**Traversal**

  Defining `resources <resource>`_ which are linked together by a  `resource tree`_ which constructs URLs which are then matched to view callables. The view callables manipulate the resource as ``request.context``

Traversal & URL Dispatch can be mixed to operate as a 3rd *URL mapping* method

**Hybrid Traversal**

  Defining *routes* (as in URL Dispatch) with match-keys/traversals that map directly to views, but leverage *resource lookup* (much like Traversal's *resource tree*) to match portions of the URL to a *resource* object which is passed to the view callable as ``request.context``. 
  
  However, Hybrid Traversal's resources are not `location-aware resources <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#location-aware>`__ as the *resource tree* isn't walked to locate the *resource*.


A pyramid application isn't bound to using just one of these 3 mapping patterns; Traversal, URL Dispatch, & Hybrid Traversal can all exist within the same application!


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
