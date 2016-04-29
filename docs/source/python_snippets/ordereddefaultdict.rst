==================
OrderedDefaultDict
==================

``OrderedDefaultDict`` is a marriage of ``collections.defaultdict`` and
``collections.OrderedDict``. It maintains the order of the keys as they're
entered while also creating default for keys that don't exist yet.

.. note::

   The dual inheritance of ``OrderedDict`` and ``defaultdict`` can cause some issues in certain set ups. 

   I'm not really sure what the instances are... but I once tried pickling ``OrderedDefaultDict`` and began getting TypeErrors on production after it worked fine in development.

   Proceed w/ caution.

.. code-block:: python

    from collections import OrderedDict, defaultdict


    class OrderedDefaultDict(OrderedDict, defaultdict):

        def __init__(self, default_factory=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.default_factory = default_factory
