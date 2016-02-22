========================
Dynamic One-To-Many Form
========================

WTForms works very well with static forms, but allowing a user to complete a
form with a one-to-many relationshipt without navigating multiple pages is a
use case not well-designed for WTForms. 

Creating a field that allows users to add as many one-to-many objects gives
them the ability to complete the form to match the model of the relationship
without navigating through a bunch of pages.


.. note::

   The DynamicFieldList references jQuery functions, and will not operate
   correctly without jQuery imported to the rendered page.


----------------
DynamicFieldList
----------------

One could achieve the desired effects of a dynamic one-to-many form by
rendering the subfield to the template and writing custom jQuery on a per-form
basis to handle deletion/addition of subforms.

If this is all going to be handled when rendering fields, why not push this off
to an inheritor of ``wtforms.fields.FieldList`` & some custom ``wtforms.widgets.Widget`` instead?

``DynamicFieldList`` is less of a custom field and more of a container that
wraps the subfield's widget & it's own widget with two custom widgets:

* ``add_field_widget_wrapper`` - wraps ``DynamicFieldList``'s widget to render
  it's sub-fields, creates a template of the subfield, and a link to add a new
  subfield to the wrapper

* ``deletable_widget_wrapper`` - wraps the subfields of ``DynamicFieldList`` to
  allow the user to delete that subfield.


The outcome of using ``DynamicFieldList`` looks something like this:

.. code-block:: html

  <!-- Without DynamicFieldList -->
  <input for="phone_numbers-1-location" />
  <input for="phone_numbers-1-number" />
  <input for="phone_numbers-2-location" />
  <input for="phone_numbers-2-number" />

  <!-- With DynamicFieldList -->
  <div id="phone_numbers_wrapper">
    <div>
      <input for="phone_numbers-1-location" />
      <input for="phone_numbers-1-number" />
      <a>Delete</a>
    </div>
    <div>
      <input for="phone_numbers-1-location" />
      <input for="phone_numbers-1-number" />
      <a>Delete</a>
    </div>
  </div>
  <a>Add</a>


This is rendered by rendering the field, and so far *cannot render the
subfields with __iter__*.

.. code-block:: mako
   
   ${form.phone_numbers()}

+++++++++++++++++++++++++
Code for DynamicFieldList
+++++++++++++++++++++++++

Below is the current code used to create dynamic_field_list

.. literalinclude:: dynamic_field_list.py
   :language: python
   :caption: dynamic_field_list.py


------------
Full Example
------------

Below is the rest of the example that runs ``dynamic_field_list.py``


.. literalinclude:: app.py
   :language: python
   :caption: app.py

.. literalinclude:: form.mako
   :language: mako
   :caption: form.mako
