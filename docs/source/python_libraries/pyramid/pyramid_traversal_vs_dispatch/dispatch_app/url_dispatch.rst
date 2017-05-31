.. _context: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-context  

.. _routes: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-route

.. _resource: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource

.. _resource tree: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource-tree


------------
URL Dispatch
------------

`URL Dispatch <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#urldispatch-chapter>`__ relies on defining more static `routes`_ which have its values
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


