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


.. literalinclude:: template_app/app_config.py
    :language: python
    :caption: Include pyramid_mako in Configurator
    :emphasize-lines: 7 


Now the view needs to be changed to use a template.


.. literalinclude:: template_app/views.py
    :language: python
    :caption: Simple view_config for rendering mako template
    :emphasize-lines: 4


Note that ``view_config(renderer='hello.mako')`` is an incomplete path: our intention is to assume that *all* mako templates referenced by ``@view_config`` are stored in ``template_app/templates/``, so we don't have to provide full context every time a template is referenced.

To do this, ``mako.directories`` needs to be passed to the application ``Configurator`` object, which can be accomplished by editing the ``.ini`` file & adding it under ``[app:main]``.

.. literalinclude:: development.ini
    :caption: Adding mako.directories to .ini
    :emphasize-lines: 5

Since the app now uses ``pyramid_mako`` to render responses, instead of sending the content from the ``view`` to the client, the ``view`` sends the template (defined in ``view_config(renderer='hello.mako')`` the blocks of information needed to render the page's content.


.. literalinclude:: template_app/templates/hello.mako
    :language: html
    :caption: Basic template for pyramid


Alternatively, one could render the template and return a ``Response`` object instead of linking the ``view`` to a template in ``view_config``.
