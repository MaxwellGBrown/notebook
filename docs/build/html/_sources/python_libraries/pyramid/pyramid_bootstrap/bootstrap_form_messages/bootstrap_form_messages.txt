================================
Bootstrap Form Validation States
================================

Bootstrap provides some really powerful `validation states <http://getbootstrap.com/css/#forms-control-validation>`__ which provide strong feedback to users.

These validation states can be applied with these classes, by adding them to
the parent element of whatever they're refering to:

* ``.has-success``
* ``.has-warning``
* ``.has-error``

Any of the below classes will receive styling based on their parent's
validation state class:

* ``.control-label``
* ``.form-control``
* ``.help-block``

Using :ref:`mako` templating and :ref:`wtforms` validation, using these blocks
to show validation errors is easy and enriching.

Below is an example of rendering a ``wtforms.Form`` object using Bootstrap Form
Validation Sates in a ``mako`` template.

.. literalinclude:: bootstrap_form_app/templates/basic.mako
   :language: mako
   :lines: 50-67
   :caption: make_form_group mako function

While it's more streamlined to define a mako function like above, some sections
of the form might need to be rendered differently, in which case you'd just
apply the same priciples above but on a per-form-group basis.

Here's the above example being applied in the template.

.. literalinclude:: bootstrap_form_app/templates/basic.mako
   :language: mako
   :lines: 33-42
   :dedent: 2
   :caption: rendering make_form_group in bootstrap form

Lastly, here's the view callable & ``wtform.Form`` used in this example.

.. literalinclude:: bootstrap_form_app/views.py
   :language: python
   :caption: view callable & form for validation states
