========================
Dynamic One-To-Many Form
========================

WTForms works very well with static forms, but finding a way to dynamically add
sub-forms in a one-to-many relationship is a non-trivial problem. Using a
somewhat-hackish solution, an interface can be made for adding and validating
subforms.

This solution uses ``mako`` and ``jQuery``.

--------------
The controller
--------------

In the controller, there are two forms defined: ``ParentForm`` which has a
one-to-many relationship with ``ChildForm`` (via ``FieldList(FormField())``). 

Sent to the template is an obstantiated ``ParentForm`` and the class
``ChildForm`` which will be used to obstantiate and render parts of the
subform.

.. literalinclude:: one_to_many.py
    :language: python
    :caption: one_to_many.py
    :lines: 4-35

Note that ``webhelpers.html.literal`` is passed to the template too, so that
when the form is rendered it's done so as raw html.


------------
The template
------------

In the rendered template, a little bit of hacky jQuery script will imitate how 
WTForms' renders the ``FieldList(FormField())`` interaction. This is done by
obstantiating the ``ChildForm`` with the key word arg ``prefix=""`` with a
prefix that will be replaced later in the javascript to match the ``name`` that
WTForms renders it's forms with. 

.. literalinclude:: form.mako
    :language: mako
    :caption: form.mako
    :emphasize-lines: 8, 10-11, 15-17, 42-44

The jQuery function ``addForm`` hacks in a new ``ChildForm`` with the new
prefix that will match it into the ``FieldList`` when being validated. This
requires no changes on the controller end; as long as the ChildForm prefix
matches what the ``Form.validate()`` is looking for it will happen naturally
and properly.

Note that *the jQuery function must exist inside the template*. The rendering
of new ChildForms and the length of entries in the ParentForm **must** be
accessable to the function. Remember, the python code is rendering jQuery code
to run, and jQuery doesn't have any access to the python objects.
