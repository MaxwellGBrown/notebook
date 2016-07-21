==================================
Automatic "active" Navigation Tabs
==================================

Bootstrap navbars & navs offer an ``active`` class to show the users which page they're currently on in relation to the navigation bar.

However, programming some reference into view callables to let the template know which page we're on just mucks up the code & template.

Using the ``request.route_url`` function, a simple jQuery function can handle this for us, without having to add any returned values in the view callables.


.. literalinclude:: ./basic_app/templates/basic.mako
   :language: mako
   :lines: 25-29
   :dedent: 2
   :caption: nav in templates/basic.mako

Above is the simple definition of the navigation bar. What's important to notice is the references to the routes in ``<a href="">``, and that the navigation bar has the id ``#navigation``, which will be referenced.

Using jQuery, ``#navigation``'s links can be traversed & matched to the url in the current window.

.. literalinclude:: ./basic_app/templates/basic.mako
   :language: javascript
   :lines: 61-67
   :dedent: 2
   :caption: nav "activation" code in templates/basic.mako

Essentially, this traverses all the ``<a>`` links within ``#navigation``'s ``<li>`` members, and checks if the href attribute matches the window's. If it does, the class "active" is added to that links parent (which is ``li`` by the nature of the selection).

.. note::

   **Warning!** If the route pages rely on query strings then some custom code needs to be written to re-match the window's href to the nav's href.

   `This stack overflow answer breaks down the window properties <http://stackoverflow.com/a/14613849>`__ which can be used to do this.
