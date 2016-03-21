.. _unittest:

========
unittest
========

``unittest`` is a python unit testing library that defines test suites for developers to run.

.. toctree::
    :maxdepth: 1

    unittest_assert_methods/unittest_assert_methods
    ../pyramid/pyramid_unittests/pyramid_unittests

Developers can use ``nose`` or ``py.test`` frameworks to run developer defined unittests.

These frameworks will automatically determine any written tests that are written. Anything that inherits from ``unittests.TestCase`` will be run. They will also check any functions or classes with the prefix ``test_``.

Basically, if it looks like it might be a test, these frameworks will try and run it!

Building nosetests with unittest
--------------------------------

Although most testing frameworks can operate perfectly fine without the ``unittest`` module, the ``unittest`` module provides a good suite to build tests under.

test fixtures using unittest.TestCase 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Any class that inherits from ``unittest.TestCase`` can take advantage of the class methods and it's structure to build  a solid **test fixture**.

test fixtures and scopes
++++++++++++++++++++++++

Modern test frameworks begin by importing a file that contains tests. To set up the scope for that module, it calls any available ``setUpModule()`` functions defined in the file/module. This scope should handle any configurations that are shared by test fixures in the same module.

``nose`` then obstantiates any test fixtures by calling the **classmethod** ``setUpClass``. This scope should handle any taxing settings that are shared within the class (e.g. database constructions, server connections)

After setting up the class, each test that is a part of the obstantiated class is prepped for by calling ``setUp``. This scope is reserved for resetting the status of the test fixture so that all tests have equal testing grounds (e.g. resetting the database cursor, changing back to a root directory).

After the test has concluded, the framework closes the test scope with ``tearDown``. After all the tests in the fixture have been run, ``tearDownClass`` is called. After all the fixtures in a module have been run, ``tearDownModule`` is called.

Below is an example of this scope using ``nose``.

::

  > nosetests -q -s test_fixtures:TestFixtures
  in module test_fixtures - setUpModule()
  in class TestFixtures - setUpClass()
  in test_1 - setUp()
  in test_1 - test_1()
  in test_1 - tearDown()
  in test_2 - setUp()
  in test_2 - test_2()
  in test_2 - tearDown()
  in class TestFixtures - tearDownClass()
  in module test_fixtures - tearDownModule()
  ----------------------------------------------------------------------
  Ran 2 tests in 0.071s

Creating setUp and tearDown methods provide a healthy testing environment for running unit tests.

using unittest.TestCase as a test fixture
+++++++++++++++++++++++++++++++++++++++++

Inheriting from ``TestCase`` also provides access to some valuable *assert* functions for the test fixture which will output what exactly caused the assertion error instead of quietly dying.

For any other tests that aren't tested via assert statements, one can call ``TestCase.fail(msg=None)``, where ``msg`` can be overridden with a custom failure message.

Below is an example of how using ``TestCase`` can provide a healthy environment to create unit tests:

.. literalinclude:: unittest_basic_tests/unittest_basic_tests.py
    :language: python
    :caption: A basic unittest file (unittest_basic_tests.py)

Using ``nose``, the test cases within the test fixture are automatically detected. There's no work that has to be done to run the tests in the correct fashion.


defining test suites
~~~~~~~~~~~~~~~~~~~~

Any number of unit tests or test fixtures can be collected in to a test suite, to be executed together. ``unittest`` has a way to define a test suite, but since nose is capable of automatic detection, test suites can be easily grouped into a module and share a scope defined by ``setUpModule``.

.. code-block:: python

    x = None

    def setUpModule():
        global x
        x = True

    def test_this():
        global x
        assert x is True

Labeling tests
--------------
It's best practice to include docstrings with your unit tests. When a test fails, the first line of the docstring is output along with the summary as to why the test failed. 

Example:

::

   ======================================================================
   FAIL: BasicTests is "Testing" while running unit tests
   ----------------------------------------------------------------------
   Traceback (most recent call last):
   File "/nose/basic_tests.py", line 28, in fail_test
      self.assertEqual(self.status, "Testing")
      AssertionError: 'Not Testing' != 'Testing'

   ----------------------------------------------------------------------
