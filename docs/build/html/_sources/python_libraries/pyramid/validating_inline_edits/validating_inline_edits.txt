=======================
Validating Inline Edits
=======================

In some cases the model of an application isn't being dictated by just one html form: perhaps theres separate methods for creation (a traditional form) and editing/updating (inline editing). 

This poses a strange set of problems for ``wtforms``: how can a ``Form`` be used to validate just one change?

Below, this page will cover one way to manage changes using ``wtforms`` from inline-edits from `X-Editable`_. For working with plain jQuery, X-Editable relies on another package `Poshytip`_, which must also be included.

.. _X-Editable: https://vitalets.github.io/x-editable/

.. _Poshytip: http://vadikom.com/demos/poshytip/


-----------------------
Working with X-Editable
-----------------------

X-Editable has a lightweight interaction w/ the web app. X-Editable is defined primaryily from an html link ``<a href='#'>`` by using ``data-*`` properties. How these ``data-*`` properties interact with the server is laid out below:

.. code-block:: html

    <a href="#" data-pk="1" data-name="username" data-url="/edit">
      FooBar
    </a>

* ``data-pk`` - the primary key of the item being interacted with. POSTs as ``pk``.
* ``data-name`` or ``id`` - the name of the value this field corrosponds to. If ``data-name`` isn't present, the plain html property ``id`` is used instead. POSTs as ``name``.
* ``data-url`` - the url in which the POST submission is sent to.

Any of the ``data-*`` properties can also be defined in the Javascript initialization of the X-Editable objects.

.. code-block:: javascript

   // data-url being defined in the jquery instead of data attribute
   $(".editable").editable({
        "url": "localhost/inline_edit",
   }) ;


In the POST request sent by X-Editable, 3 things will be sent at a minimum:

* ``pk`` - the ``data-pk`` attribute
* ``name`` - the ``data-name`` or ``id`` attribute
* ``value`` - the value retrieved from the X-Editable input

Additional information can be sent with the POST requests if specified in the ``params`` argument on X-Editable initialization.



------------------------------
The View Handling Inline Edits
------------------------------

With a constructed model and a form to match a model object, we can use X-Editable's inline-edits to spoof making a single change to a form, and then validating that form.

.. literalinclude:: inline_app/views.py
    :language: python
    :caption: Changing a single Field.data in a wtforms.Form
    :emphasize-lines: 10-12, 15 
    :lines: 25-51

The submitted ``pk`` value is used to retrieve the object that's being edited from the ORM (pseduo-orm in this example). 

To validate a change to this object, the form is populated with the current values of the object. 

Next,the corrosponding field from the form is retrieved using ``getattr()`` and the POSTed ``name`` value (which should corrospond to the ``__name__`` of the ORM field and the form field). The POSTed ``value`` is then used to overwrite the current form value using ``field.process_formdata([value])``.

.. note::
   ``.process_formdata`` takes a list as an argument because when retrieving submitted params in a request, there can be more than 1 value for that key. 

   ``.process_formdata`` will always use the item at index 0, unless overwritten.


After updating the formdata with the POSTed values, the form is validated. If there are no errors, ``setattr()`` is run using the ORM object, ``name``, and ``value``, and then the change is committed. If validation fails, nothing is changed!

.. note::
   The initialization of ``wtforms.Form`` sometimes has trouble reading data from relationships between ORM objects. 

   However, if the object can be converted to a dictionary, wtforms.Form uses it's ``**kwargs`` as form data on itialization.

------------
Full Example
------------

.. literalinclude:: inline_app/views.py
  :language: python
  :caption: Inline Edit Views (inline_app/views.py)


.. literalinclude:: inline_app/templates/index.mako
  :language: mako
  :caption: Inline Edit Template (inline_app/templates/index.mako)
