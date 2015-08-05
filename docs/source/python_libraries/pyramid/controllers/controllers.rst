========================
Pylons-style controllers
========================

Pyramid is void of terminology relating to the **controller** of the previous pylons implementation. However, there is often a need to group logically related views. This example will cover grouping views into python classes, essentially making a formal controller.


Setting up the views
--------------------

To group logically related views into a class there are two decorators that can be leveraged from ``pyramid.view``. ``view_config``, a class decorator, and ``view_defaults``.


.. literalinclude:: basic_app/views.py
    :language: python
    :caption: basic_app/views.py
    :emphasize-lines: 4, 9, 13


The decorators controll how our new ``class`` view interacts with the app ``Configurator``. 

``view_defaults()`` is a ``class`` decorator that sets the defaults for all of the class methods that are used as views. In this example, ``view_defaults(renderer='templates/home.mako')`` sets the default template for all of the view methods.

``view_config()`` is a ``function`` decorator that sets the information for that method/view. In the example above, ``route_name`` is being defined which matches up to the routes defined in the ``Configurator``. ``view_config()`` overrides any default settings set in ``view_defaults()``.


Add the new views to the controller
###################################

Because there are multiple views now, there needs to be additional routes in the ``Configurator`` in ``basic_app/setup_app.py``


.. literalinclude:: basic_app/setup_app.py
    :language: python
    :caption: basic_app/setup_app.py


Now in the ``Configurator`` there are two defined routes that match the routes defined by the ``view_config()`` decorators:

* visiting the ``/`` route will render ``BasicAppController.home()``
* visiting the ``/howdy`` route will render ``BasicAppController.hello()``


The default template for the Controller
#######################################

/templates/home.mako is the template that is shared in the Controller as defined by the class decorator ``view_defaults()``. This is the template that matches that controller.


.. literalinclude:: basic_app/templates/home.mako
    :language: html
    :caption: basic_app/templates/home.mako


nosetests for the Controller
----------------------------

Setting up unit tests to run with Controller style views requires a little extra work. Instead of running a request through a view function, the Controller class needs to be initialized with the request and then the view method needs to be called.

Functional tests don't change at all, because with functional tests, you're sending a path to the application to handle, not to a python function.


.. literalinclude:: basic_app/tests.py
    :language: python
    :caption: basic_app/tests.py
    :emphasize-lines: 16-18, 25-27  


