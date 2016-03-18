.. _pyramid_simple_ajax:

Simple Ajax Process w/ Pyramid
==============================

Some server-side processes can take quite a while to run. From a user's perspective it's very hard to tell if anything is happening.

This example goes over how to set up an ajax request-response cycle & displays the status of the process w/ a Bootstrap loading bar.

.. note::

  This example references...
    * :ref:`mako <mako>`
    * JavaScript & jQuery
    * `Bootstrap <http://getbootstrap.com>`_ (specifically `progress bars <http://getbootstrap.com/components/#progress>`_)


This example can be found in ``/docs/source/python_libraries/examples/pyramid_simple_ajax/``


Ajax View Callable
------------------

In this example, the view callable is built to take repeated requests from the client asking for a "percentage" of completion. 

Each request to the view callable moves the process along by another increment of work until the process is 100% complete, in which the client will stop sending requests to increment the work along.

Note that since this example is lightweight, the server is spoofing a ``Flask`` session.

.. literalinclude:: basic_app/views.py
  :language: python
  :caption: basic_app/views.py Ajax View Callable
  :lines: 17-38

This view callable will create a new queue based on the form's parameters if there is no queue already, or pop the next item in the queue if one already exists.  Thus, it becomes the client's responsibility to stop sending requests once the process is completed.

Also note the view_config's renderer, so it can communicate appropriately w/ JSON.

.. code-block:: python

  @view_config(route_name="ajax_process", renderer='json')



HTML Progress Bar & Form
------------------------

This template uses a `bootstrap progress bar <http://getbootstrap.com/components/#progress>`_ to display the current status of the progress.

.. literalinclude:: basic_app/templates/index.mako
  :language: html
  :caption: basic_app/templates/index.mako Progress Bar
  :lines: 18-22

The actual bar that displays the progress is ``#progress_bar``, while ``#progress`` is the container that wraps that. The width of the bar changes by editing ``style="width: 0%;"``.


The form itself is just a basic form, which with jQuery can be overridden for Ajax.

.. literalinclude:: basic_app/templates/index.mako
  :language: html
  :caption: basic_app/templates/index.mako Form
  :lines: 24-44

Note that the inputs (including the submit) are wrapped in a ``<fieldset>`` with a specific id. This is so they can be disabled while the Ajax process is happening. By disabling a fieldset, all of it's children are also disabled.


jQuery Ajax Form Submission
---------------------------

Without an Ajax loop, the form won't interact w/ the view callable very well.

jQuery can be used to listen for form submission & override it with an Ajax loop that will perform how we expect.

.. literalinclude:: basic_app/templates/index.mako
  :language: javascript
  :caption: basic_app/templates/index.mako Inline Javascript
  :lines: 49-96

Below is the order of operations after a user clicks "Submit":

1. The original form submission is canceled so an Ajax loop can be started instead
2. The progress bar is reset to it's original state (no extra-classes, 0%)
3. The form is disabled after serializing it's data & getting it's action url
4. The function ``send_request()`` is defined based on form data
5. ``send_request()`` is called starting/continuing the Ajax loop
6. The server responds & the loading bar is updated
7. If the server responds with anything less that 100.0 percent, return back to step 5
8. After 100.0 percent, a "completed" class is added to the loading bar and the form is unlocked

.. note:: 
  Some more complex processes might need multiple view callables in more of a waterfall process. As long as they're wrapped in jQuery.ajax's ``success`` function, they will not be called until a response is received from the server.
  
  For example, repeated calls for file generation then a final request to a different process to retrieve said file.

  Or, for a more complex example: a linear this-then-that process with multiple view callables. Defining the jQuery.ajax's ``success`` funciton separately and nesting a few might be best, so that way a jQuery.ajax ``error`` function can be shared between them.


Full Example
------------

.. literalinclude:: basic_app/templates/index.mako
  :language: html
  :caption: basic_app/templates/index.mako

.. literalinclude:: basic_app/views.py
  :language: python
  :caption: basic_app/views.py
