======================================
Mako Template Inheritance & Namespaces
======================================

Mako templates can both inherit namespaces from other templates, import namespaces from other templates, or pass their namespaces on to the next inheritor in the chain.

This document is a curated set of notes from mako's `namespaces <http://docs.makotemplates.org/en/latest/namespaces.html>`__ and `inheritance <http://docs.makotemplates.org/en/latest/inheritance.html>`__ documentation to define the parts that *I* find necessary to know. 

----------
Namespaces
----------

A **Namespace** in mako refers to organized groups of mako ``def`` and ``block`` objects.

Each template has it's own namespace, but can also get access to other namespaces either through imports or template inheritance.


Importing a Template as a Namespace
+++++++++++++++++++++++++++++++++++

A ``<%namespace/>`` tag imports all the defined ``block`` and ``def`` from another template.

.. code-block:: mako

    ## hello.mako
    <%def name="hello_world()">
      Hello World 
    </%def>


    ## index.mako
    <%namespace name="foo" file="hello.mako"/>

    foo.hello_world: ${foo.hello_world()}


Importing a Python Module as a Namespace
++++++++++++++++++++++++++++++++++++++++

Namespaces can also import regular python functions from modules. 

These callables need to take at least one argument, ``context`` and instance of Mako's `Context <http://docs.makotemplates.org/en/latest/runtime.html#mako.runtime.Context>`__.

.. code-block:: python

    # some/module.py
    def my_tag(context):
        context.write("hello world")
        return ""

If ``my_tag()`` is called in a template, anything passed with ``Context.write()`` and the ``return`` value are rendered to the template.

After that, importing and calling the module is much the same as importing another template's namespace

.. code-block:: mako

    ## template.mako
    <%namespace name="hw" module="some.module"/>

    ${hw.my_tag()}


If this module needs to be aware of the caller ("embedded content" context, e.g. self, parent, next) then the ``@supports_caller`` decorator is necessary.

.. code-block:: python

    # some/module.py

    from mako.runtime import supports_caller

    @supports_caller
    def my_tag(context):
        context.write("<div>")
        context['caller'].body()
        context.write("</div>")
        return ""


The body() Method
+++++++++++++++++

Every namespace that is generated from a template contains a method called ``body()``.

This method corresponds to the main body of the template and plays an important role in inheritance.

By default ``body()`` takes no positional arguments and dumps all keyword arguments to a variable called ``pageargs`` which are used to render templates.

To define the pageargs and the necessary variables to execute a template, define a ``<%page>`` tag:

.. code-block:: mako

    <%page args="x, y, someval=8, scope='foo', **kwargs"/>


Defining the ``<%page>`` tag will require that these arguments are supplied when rendered as a top-level template


.. code-block:: python

    >>> from mako.template import Template
    >>> template = Template(filename="foo.mako")
    >>> template.render()
    TypeError: render_body() missing 2 required positional arguments: 'x' and 'y'
    >>> template.render(5, y=10, someval=15, delta=7)
    "foo.mako's body()"


This constraint also applies for any call to ``body()`` using mako's built-in namespaces.

.. code-block:: mako

    ${self.body(5, y=10, someval=15, delta=7)}


Built-in Namespaces
+++++++++++++++++++

Every template includes the built-in ``local`` and ``self`` namespaces.

Since these are more pertinant to inheritance than namespaces they're covered in :ref:`inheritance_namespaces`


-----------
Inheritance
-----------

Template inheritance allows the creation of **inheritance chains** between templates.

If ``child_template`` inherits from ``parent_template``, then ``child_template`` sends all executional control to ``parent_template``, who then makes the decisions on what resources will be executed.

.. code-block:: mako

    ## index.haml
    <%inherit file="base.html">

    <%def name="foo()">
      Hello World
    </%def>


    ## base.html
    <html>
      <body>
        ${self.foo()}
      </body>
    </html>


.. _inheritance_namespaces:

Inheritance Namespaces
++++++++++++++++++++++

When using template inheritance, the inheritance chain is read and several built-in template namespaces are provided.

Understanding these namespaces is the key to creating a good inheritance structure and well-organized templates.


local
~~~~~

The ``local`` namespace is the namespace for the currently executing template. This includes all the top-level defs defined in the template as well as the ``body()`` function.


self
~~~~

In a template without inheritance, ``self`` is synonymous with ``local``.

If inheritance is used, ``self`` refers to the *topmost template in the inheritance chain*.

This is useful when various "method" calls have been overridden at various points in an inheritance chain.


next
~~~~

``next`` refers to the namespace of the template **immediately following** the current template.

This allows for an inheritance chain of templates to insert layouts of the rest of the template chain into itself.

.. code-block:: mako
    :emphasize-lines: 4

    ## base.haml
    <html>
      <body>
        ${next.body()}
      </body>
    </html>


parent
~~~~~~

``parent`` refers to the namespace of the template **immediately preceding** the current template.

This allows templates to call and extend upon overridden blocks or defs.

.. code-block:: mako
    :emphasize-lines: 6

    ## index.mako
    <inherit file="layout.mako"/>

    <%def name="toolbar()">
      ## call layout.mako's toolbar()
      ${parent.toolbar()}
      <li>Selection 4</li>
      <li>Selection 5</li>
    </%def>
