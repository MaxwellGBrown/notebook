.. _context: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-context  

.. _routes: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-route

.. _resource: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource

.. _resource tree: http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource-tree


==========================
Traversal vs. URL Dispatch
==========================

Pyramid is a marraige of ``repoze.bfg`` and ``pylons``. 

Because of this marriage, there's two fundamentally different ways to handle application structure:

* **URL Dispatch**: defined by *routes* (a concept inherited from ``pylons``)
* **Traversal**: defined by *resources* (a concept inherited from ``repoze.bfg``)

Because pyramid is a *micro-framework* and does not restrict developrs to a specific structure, URL Dispatch and Traversal can coexist withing the same application as Hybrid Traversal.

* **Hybrid Traversal**: defined by *routes* that have their own *resource* structure


This doc & it's children aim at demistifying the similarities and differences between these structures.

.. toctree::
   :maxdepth: 2

   dispatch_app/url_dispatch.rst
   traversal_app/traversal.rst
   hybrid_app/hybrid_traversal.rst


---------------------------
Which Should I Use and Why?
---------------------------

**Which type is most appropriate for my application?**

A pyramid application isn't bound to using just one of these 3 mapping patterns; Traversal, URL Dispatch, & Hybrid Traversal can all exist within the same application!

That being said, it's usually best to start with one of URL Dispatch or Traversal. When the need arises to borrow features from the other structure, borrow the functionality as needed!

Below will help you decide which scheme to start off with.

+++++++++++++++++++++++++++++++
When Should I Use URL Dispatch?
+++++++++++++++++++++++++++++++

**Most Always**

URL Dispatch is similar to ``pylons``'s concept of routes.

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

Traversal is the baby of ``repoze.bfg``.

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



