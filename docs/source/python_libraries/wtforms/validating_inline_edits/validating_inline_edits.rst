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
    :caption: inline_app/views.py
    :lines: 25-50
    :emphasize-lines: 32-34, 36

The submitted ``pk`` value is used to retrieve the object that's being edited from the ORM (pseduo-orm in this example). Then, the value of the object is changed using ``setattr()``: the ``name`` submitted in the POST matches the objects class member and the ``value`` matches what the new value should be. 

After changing the objects values, it's used as the initializing argument to the form object that matches the model, and then validated. If there's an error in the single change made to the object, it will not validate. 

Some more complex models might need a bit of coercing to work with their form. In these instances, any data for the form's fields can be supplied as kwargs of a matching name.


------------
Full Example
------------

.. literalinclude:: inline_app/views.py
  :language: python
  :caption: inline_app/views.py


.. literalinclude:: inline_app/templates/index.mako
  :language: mako
  :caption: inline_app/templates/index.mako
