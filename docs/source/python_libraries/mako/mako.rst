====
mako
====

Mako is a templating library. It works best as a markup language templater.

.. toctree::
  :maxdepth: 1
  :glob:

  examples/*


Everything you need to know in 1 template
-----------------------------------------

basic/template_file.mako
~~~~~~~~~~~~~~~~~~

.. code-block:: mako

    <%inherit file="base.mako"/>
    <%
        rows = [[v for v in range(0,10)] for row in range(0,10)]
    %>
    <h1>${header_1}</h1>
    <table>
        % for row in rows:
        ${makerow(row)}
        % endfor
    </table>

    <%def name="makerow(row)">
        <tr>
            % for name in row:
            <td>${name}</td>\
            % endfor
        </tr>
    </%def>

``template_file.mako`` shows off all the basics of mako templating.

To render a template like this, the base.html needs to be defined too.

basic/base.mako
~~~~~~~~~

.. code-block:: mako

    <HTML>
        <head>
            ${self.head()}
        </head>

        <body>
            ${next.body()}
        </body>
    </HTML>

    <%def name="head()">
        <title>Mako Example</title>
    </%def>

Note that ``self`` refers to the current template and ``next`` refers to the next inherited template.

``next.body()`` is the default and un-scoped definition for the whole template. So, unlike ``self.head()`` which is defined, the inheriting template doesn't need to define ``self.body()`` (unless you really want to).

basic/main.py
~~~~~~~

.. code-block:: python

    import os.path

    from mako.template import Template
    from mako.lookup import TemplateLookup

    # set up a lookup so template_file.mako can find base.mako
    this_dir = os.path.dirname(os.path.realpath(__file__))
    lookup = TemplateLookup(directories=[this_dir])

    # render the template
    t = Template(filename="template_file.mako")
    print t.render(header_1="Hello World")
