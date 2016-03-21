.. _form_as_separate_template:

=====================================
Separate Template for Rendering Forms
=====================================

The way WTForms is set up, it's easier to re-render the whole page to show errors to a form that failed server-side validation. 

For small and lightweight pages, this isn't much of an issue. However, for heavy pages with a lot of action and javascript, this might not be acceptable.

This is just one use case for housing the form in it's own template & view callable for AJAX calls.

.. note::

  This example builds off the following knowladge bases:

  * :ref:`pyramid <pyramid>`
  * jQuery
  * :ref:`WTForms <wtforms>`

  Understanding the above will improve the "brilliance" of this examples magic.


-------------------------------
Form HTML Snippets as Templates
-------------------------------

Below shows what this html snippet would look like with only the ``firstname`` field & its errors rendered.

.. literalinclude:: form.mako
   :language: mako
   :caption: A Form as an HTML Snippet Template
   :lines: 1-13, 44-45 

Again, the advantage is that based off the different states of the active form (empty, pre-populated, invalid, etc.), the form can be rendered in an existing page without having to reload the whole page & it's dependencies.


---------------------------------------------------
The View Callable That Serves the Form HTML Snippet
---------------------------------------------------

Since this form can be retrieved in a few different states (empty, invalid form data with errors, if you're editing an existing item), a special view callable is made to handle the rendering of the form.

.. literalinclude:: form_as_separate_template.py
   :language: python
   :caption: /form view callable
   :lines: 28-47

On receiving a GET request, the view returns a 200 response with an empty form (and a friendly message!). On a POST request, the form will try to validate and add the submission to the "database". If it does not validate, it will respond with a 422 (BAD) status and re-render the form template with the invalid data and errors.

The view will render the template regardless. It leaves how that response is rendered up to the page requesting it.

.. note::

   With a little extra elbow grease, this view callable can be expanded to pre-populate the form with an existing object from the "database" for an edit function!


----------------------------------------------
Using jQuery to Operate the Form HTML Snippets
----------------------------------------------

Since it's up to the page to determine what happens when loading/submitting the form's html snippet, some jQuery will operate that real nicely.

First the form needs to be loaded when document is "ready":

.. literalinclude:: index.mako
   :language: javascript
   :caption: jQuery load empty form on page load
   :lines: 8-14

Note that the GET method (``$.get()``)is being used to get the empty form via AJAX.


Since the HTML used to render the form doesn't exist by ``$(document).ready()``, a global listener for the ``document`` needs to be set up, so any actions the page is listening for will be handled on DOM objects that haven't necessarily been rendered yet.

.. literalinclude:: index.mako
   :language: javascript
   :caption: jQuery AJAX form submission/reloading
   :lines: 15-31

On success (when the view callable's status is ``200 OK``), the AJAX request refreshes the whole page, because the list of all submissions is static to the template. Other setups may reload data differently.

On error (when the view callable's status is ``422 BAD``), the AJAX handler uses the responseText (which is the new HTML snippet of the form with the invalid information and displayed error messages) and replaces the current form HTML with the new HTML.

.. note::
   **Reminder**: the burden of handling the HTML snippets is on the page & not the view. 


------------
Full Example
------------

Below is a full include of the example files.

.. literalinclude:: form_as_separate_template.py
   :language: python
   :caption: form_as_separate_template.py (Webapp & view callables)

.. literalinclude:: index.mako
   :language: mako
   :caption: index.mako (HTML page template)

.. literalinclude:: form.mako
   :language: mako
   :caption: form.mako (Form template)
