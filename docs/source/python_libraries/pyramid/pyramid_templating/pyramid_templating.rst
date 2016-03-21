.. _mako_templates_and_pyramid:

Mako Templates & Pyramid
------------------------

Pyramid comes packed with ``chameleon``. ``jinja2``, and ``mako``. This example will use ``mako``. 

First, ``setup.py`` needs to be updated to require the templating tool.


.. literalinclude:: setup.py
    :language: python
    :caption: setup.py
    :emphasize-lines: 5


After that, the application ``Configurator`` needs to know the templating tool being used. Note that ``pyramid_mako`` doesn't come standard and needs to be installed with ``$ pip install pyramid_mako``.


.. literalinclude:: basic_app/setup_app.py
    :language: python
    :caption: Include pyramid_mako in Configurator
    :emphasize-lines: 7 


Now the view needs to be changed to use a template.


.. literalinclude:: basic_app/views.py
    :language: python
    :caption: Simple view_config for rendering mako template
    :emphasize-lines: 4


Since the app now uses ``pyramid_mako`` to render responses, instead of sending the content from the ``view`` to the client, the ``view`` sends the template (defined in ``view_config(renderer='templates/hello.mako')`` the blocks of information needed to render the page's content.


.. literalinclude:: basic_app/templates/hello.mako
    :language: html
    :caption: Basic template for pyramid


Alternatively, one could render the template and return a ``Response`` object instead of linking the ``view`` to a template in ``view_config``.
