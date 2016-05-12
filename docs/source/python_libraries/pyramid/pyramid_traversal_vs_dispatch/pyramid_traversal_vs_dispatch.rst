==========================
Traversal vs. URL Dispatch
==========================

Pyramid has two main methods to manage *mapping URLs to view callables*:

**URL Dispatch**

  Defining `routes <http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-route>`_ and their parameters to match URLs to view callables.

**Traversal**

  Defining `resources <http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource>`__ which are linked together by a  `resource tree <http://docs.pylonsproject.org/projects/pyramid/en/latest/glossary.html#term-resource-tree>`__ which constructs URLs which are then matched to view callables. The view callables manipulate the resource as ``request.context``

Traversal & URL Dispatch can be mixed to operate as a 3rd *URL mapping* method

**Hybrid Traversal**

  Defining *routes* (as in URL Dispatch) with match-keys/traversals that map directly to views, but leverage *resource lookup* (much like Traversal's *resource tree*) to match portions of the URL to a *resource* object which is passed to the view callable as ``request.context``. 
  
  However, Hybrid Traversal's resources are not `location-aware resources <http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/resources.html#location-aware>`__ as the *resource tree* isn't walked to locate the *resource*.


A pyramid application isn't bound to using just one of these 3 mapping patterns; Traversal, URL Dispatch, & Hybrid Traversal can all exist within the same application!
