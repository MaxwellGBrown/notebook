=========
nosetests
=========

``nose`` is a python unit testing framework that runs unit tests. Install it by running ``pip install nose`` and run it in the shell with ``$ nosetests``.

.. toctree::
    :maxdepth: 1
    :glob:

    ./*/*

``nose`` will automatically determine any written tests that are written. Anything that inherits from ``unittests.TestCase`` will be run by ``nose``. ``nose`` will also check any functions with the prefix ``test_``. Basically, if it looks like it might be a test, ``nose`` will try and run it!

Building tests
--------------

It's good practice to set up tests in a testing ``class``. This way tests can operate within a controlled testing environment, as dictated by ``TestCase.setUp()`` and ``TestCase.tearDown()``. Inheriting from ``TestCase`` also provides access to some valuable *assert* functions which will output what exactly caused the assertion error instead of quietly dying.


.. literalinclude:: basic_tests.py
    :language: python
    :caption: basic_tests.py

TestCase assert methods
~~~~~~~~~~~~~~~~~~~~~~~

Below is all of the assert methods part of the class ``TestCase`` as of python 2.7

========================    ====================
Method                      Checks that...
========================    ====================
assertEqual(a,b)            a == b
assertNotEqual(a, b)        a != b
assertTrue(x)               bool(x) is True
assertFalse(x)              bool(x) is False
assertIs(a, b)              a is b
assertIsNot(a, b)           a is not b
assertIsNone(x)             x is None
assertIsNotNone(x)          x is not None
assertIn(a, b)              a in b
assertNotIn(a, b)           a not in b
assertIsInstance(a, b)      isinstance(a, b)
assertNotIsInstance(a,b)    not isinstance(a, b)
========================    ====================


What to write unit tests for
----------------------------
This topic desires more time and attention than I currently have to explain to my future self...
