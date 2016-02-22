.. _wtforms:

=======
wtforms
=======

``wtforms`` is an HTML form building and validation tool. 

Note that examples for this package may reference :ref:`mako <mako>` templating or :ref:`pyramid <pyramid>` for server.

**Examples**

.. toctree::
    :maxdepth: 1

    examples/wtforms_dynamic_select_fields/dynamic_select_fields
    examples/wtforms_dynamic_field_list/dynamic_field_list
    examples/validating_inline_edits/validating_inline_edits
    examples/form_as_separate_template/form_as_separate_template


----------
The Basics
----------

The following basic information on using ``wtforms`` is gleaned from the `Crash Course <https://wtforms.readthedocs.org/en/latest/crash_course.html>`_ in wtforms documentation.

^^^^^^^^^^^^^^^
Defining a form
^^^^^^^^^^^^^^^

The below information is gleaned from ``wtforms``'s 

The basic blocks of ``wtforms`` is the ``Form``, the ``Field``, the ``Widget``, which is part of the ``Field``, and the ``Validator``.

The block below shows how a ``Form`` is defined using ``Fields`` and ``Validators``:

.. code-block:: python

    from wtforms import Form, BooleanField, StringField, validators

    class RegistrationForm(Form):
        username = StringField("Username", [validators.Length(min=5, max=25)])
        email = StringField("Email Address", [validators.Length(min=6, max=35)])
        accept = BooleanField("I accept", [validators.InputRequired()])


The attributes and methods that belong to a ``Form`` are helpful when rendering templates, updating databases, or validating a filled out form.

::

    >>> form = RegistrationForm()
    >>> form['username']
    <wtforms.fields.TextField object at 0x123ABCD>
    >>> form.username.data
    u'test'
    >>> form.validate()
    False
    >>> form.errors
    {'username': [u'Field must be at least 5 characters long.']}


^^^^^^^^^^^^^^^^
Rendering Fields
^^^^^^^^^^^^^^^^

There are two option to rendering a field in a form.

    1. It can be rendered as a string
    2. The field can be rendered with ``__call__()``

Using ``__call__()``, a field can be provided HTML parameters when rendered.

::
    
    >>> form = RegistrationForm(username="Test")
    >>> str(form.username)
    '<input id="username" name="username" type="text" value="Test" />'
    >>> form.content(class_="bar")
    '<input class="bar" id="username" name="username" type="text" value="Test" />'


Applying these traits to a template proves very powerful results. When rendering the form, you can take advantage of HTML's ``<label>`` via a field's ``.label`` attribute, easily render all of the validation errors with an input using a field's ``.errors`` attribute, and use a fields ``__call__()`` method.

The below example is how one might render a form using ``mako``.

.. code-block:: mako

    <form method="POST" action="/register">
        <div>
        ${form.username.label}: ${form.username()}
        % if form.username.errors:
            <ul class="errors">
                % for error in form.username.errors:
                    <li>
                        ${error}
                    </li>
                % endfor
            </ul>
        % endif
        </div>
    </form>


^^^^^^^^^^^^^^^^^^^^^^^^
Create/Edit with wtforms
^^^^^^^^^^^^^^^^^^^^^^^^

``wtforms`` can populate and validate a ``Form`` with the submitted POST data that matches the ``Form``. After the validation the data can be taken from the ``Form``'s ``Fields`` to manipulate as desired.

.. code-block:: python

    def register(request):
        form = RegistrationForm(request.POST)
        if request.method == "POST" and form.validate():
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.save()
            redirect('register')
        return render_response('register.html', form=form)


When using forms for editing objects, the ``Form`` and it's ``Fields`` can have it's data pre-populated by an object. Also, the form can update the object using the method ``Form.populate_obj()``.


.. code-block:: python

    def edit_profile(request):
        user = request.current_user
        form = ProfileForm(request.POST, user)
        if request.method == "POST" and form.validate():
            form.populate_obj(user)
            user.save()
            redirect('edit_profile')
        return render_response('edit_profile.html', form=form)


