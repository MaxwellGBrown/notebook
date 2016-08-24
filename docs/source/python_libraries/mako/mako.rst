.. _mako:

====
mako
====

Mako is a templating library. It works best as a markup language templater.

**Examples**


.. toctree::
  :maxdepth: 1

  mako_template_inheritance
  ../pyramid/pyramid_templating/pyramid_templating
  Mako & Bootstrap Validation States <../pyramid/pyramid_bootstrap/bootstrap_form_messages/bootstrap_form_messages>
  ../pyramid/form_as_separate_template/form_as_separate_template


Everything you need to know in one template
-------------------------------------------


.. literalinclude:: mako_basic/template_file.mako
    :caption: mako_basic/template_file.mako
    :language: mako


``template_file.mako`` shows off all the basics of mako templating.


Inheriting from a different template
####################################

To render a template like ``basic/template_file.mako``, the base.mako needs to be defined too.


.. literalinclude:: mako_basic/base.mako
    :caption: mako_basic/base.mako
    :language: mako


Note that ``self`` refers to the current template and ``next`` refers to the next inherited template.

``next.body()`` is the default and un-scoped definition for the whole template. So, unlike ``self.head()`` which is defined, the inheriting template doesn't need to define ``self.body()`` (unless you really want to).

Rendering a template
####################

Render ``template_file.mako`` by reading it as a ``mako.template.Template``. 

Because ``template_file.mako`` inherits from ``base.mako``, a correctly configured ``mako.lookup.TemplateLookup`` needs to be passed to the ``Template`` object.


.. literalinclude:: mako_basic/main.py
    :caption: mako_basic/main.py
    :language: python
