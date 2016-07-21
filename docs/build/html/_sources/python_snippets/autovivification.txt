================
Autovivification
================

`Autovivification <https://en.wikipedia.org/wiki/Autovivification>`__ is a dictionary that will recursively create sublevels of itself when accessing keys that don't exist (essentially a recursive defaultdict of ).  

Autovivification
----------------

Based off the `wikipedia example <https://en.wikipedia.org/wiki/Autovivification#Python>`__ here's autovivification with ``OrderedDefaultDict``


.. code-block:: python

    from collections import defaultdict

    def autovivification():
        return defaultdict(autovivification)

    >>> x = autovivification()
    >>> x['a']['b']['c'] = "ABC"  # no need to assign subkeys beforehand! 


De-vivification
---------------

Sometimes vivification can cause issues w/ iteration/printing/__repr__, so it's important to be able to "de-vivificate" an autovivification.

.. code-block:: python

    def devivificate(vivificated):
        devivificated = dict()
        for key in sorted([k for k in vivificated.keys()]):
            if isinstance(vivificated[key], dict):
                devivificated[key] = devivificate(vivificated[key])
            else:
                devivificated[key] = vivificated[key]
        return devivificated
