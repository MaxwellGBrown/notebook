=====================
Dynamic Select Fields
=====================

WTForms does this silly thing where any field that needs a ``choices`` kwarg on initiation (e.g. ``SelectField``, ``SelectMultipleField``) will only use that set of choices. 

This does not cater well to complex forms that have subforms. For example, if a subform has a field that requires ``choices`` that field has already been obstantiated, and thus is stuck to that strict set of ``choices``. 

The very easy workaround to this issue is to override that sub-forms ``__init__`` function to self-assign the choices.

.. code-block:: python
    :emphasize-lines: 8-11

    from wtforms import SelectField, FormField, FieldList
    import random


    class SubForm(Form):
        numbers = SelectField("Numbers", choices=[])

        def __init__(self, *args, **kwargs):
            super(SubForm, self).__init__(*args, **kwargs)
            new_choices = [(n, n) for n in range(random.randint(0,100), random.randint(0,101))]
            self.choices = new_choices

    class MainForm(Form):
        subforms = FieldList(FormField(SubForm))
        

By overriding the ``__init__`` function, every time ``MainForm.__init__()`` and ``MainForm.validate()`` is handled (see: Everytime) the set of choices will be updated!
