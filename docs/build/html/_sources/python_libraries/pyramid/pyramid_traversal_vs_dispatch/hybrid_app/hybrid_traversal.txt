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

This is a Hybrid Traversal route, in that it's a route. Otherwise, this route is completely defined by the traversal of the request's path segments.

Note that when using a "pure traversal" hybrid route, all resources in the route's resource tree need to be `location aware <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#location-aware>`.

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


Doing this you can tightly control the arguments from the route pattern that are supplied to the ``__getitem__`` methods of the context. This is probably the "middle ground" between traversal and URL Dispatch, although there's arguably little benefit to using routes like this instead of :ref:`URL Dispatch resource location <url_dispatch_resource_location>`.


^^^^^^^^^^^^^^^^^^^^^
Matchdict & Traversal
^^^^^^^^^^^^^^^^^^^^^

Sometimes routes desire static path segments between URL Matchdict values and the traversal wildcard. 

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

    @view_config(route_name='both', name="traversal_view", context=Resource)
    def traversal_view(request):
        return Response()

    # URL Generation
    request.resource_url(resource, route_name='both', route_kw={'foo': 'Hello'})
    request.resource_url(resource, "traversal_view", route_nmae="both",
            context=Resource)


