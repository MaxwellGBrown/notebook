TestCase assert methods
=======================

Below is all of the assert methods part of the class ``TestCase`` as of python 2.7

=======================================    ===============================
Method                                     Asserts that...
=======================================    ===============================
assertEqual(a,b)                           a == b
assertNotEqual(a, b)                       a != b
assertGreater(a, b)                        a > b
assertGreaterEqual(a, b)                   a >= b
assertLess(a, b)                           a < b
assertLessEqual(a, b)                      a <= b
assertTrue(x)                              bool(x) is True
assertFalse(x)                             bool(x) is False
assertIs(a, b)                             a is b
assertIsNot(a, b)                          a is not b
assertIsNone(x)                            x is None
assertIsNotNone(x)                         x is not None
assertIn(a, b)                             a in b
assertNotIn(a, b)                          a not in b
assertItemsEqual(a, b)                     sorted(a) == sorted(b)
assertDictContainsSubset(a, b)             all key/values in a exist in b
assertIsInstance(a, b)                     isinstance(a, b)
assertNotIsInstance(a,b)                   not isinstance(a, b)
assertRaises(exc, fun, \*args, \**kwds)    fun(\*args, \**kwds) raises exc
=======================================    ===============================

Additional features for TestCase assertion
------------------------------------------

assertRaises(exc)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``assertRaises(exc)`` can also be used to define a scope to check for exceptions.

.. code-block:: python

    with self.assertRaises(SomeException):
        do_something()

    with self.assertRaises(SomeException) as cm:
        do_something()
    the_exception = cm.exception
    self.assertEqual(the_exception.error_code, 3)

type equality functions
~~~~~~~~~~~~~~~~~~~~~~~

the method ``TestCase.addTypeEqualityFunc(typeobj, function)`` registers a type-specific method called by ``assertEqual()`` to check if two objects of the same **typeobj** compare equal. **function** must take two positional arguments and a third **msg=None** keyword argument. It must raise ``self.failureException(msg)`` on inequality.

.. code-block:: python

    class CustomClass(object):
        def __init__(self, x):
            self.x = x

    class exampleTestCase(unittest.TestCase):

        def _custom_class_is_equal(a, b, msg=None):
            if a.x != b.x:
                msg = "{}.x == {}.x is False".format(a, b)
                self.failureException(msg)

        def setUp(self):
            self.addTypeEqualityFunc(CustomClass, self._custom_class_is_equal)

Some type equality functions have already been defined, however it's not necessary to invoke these methods directly, as ``assertEqual()`` will call them. They may be useful to call when defining a type equality function for a custom class.

===================================  ==========================
Method                               Used to compare
===================================  ==========================
assertMultiLineEqual(a, b)           strings
assertSequenceEqual(a, b)            sequences
assertListEqual(a, b)                lists
assertTupleEqual(a, b)               tuples
assertSetEqual(a, b)                 sets
assertDictEqual(a, b)                dicts
===================================  ==========================

regex assert methods
~~~~~~~~~~~~~~~~~~~~

Regexes can also be searched, matched, and tested with TestCase.

================================================  ===============================================================
Method                                            Checks that...
================================================  ===============================================================
assertRegexpMatches(s, r)                         r.search(s)
assertNotRegexpMatches(s, r)                      not r.search(s)
assertRaisesRegexp(exc, r, fun, \*args, \**kwds)  fun(\*args, \**kwds) raises exc and the message matches regex r
================================================  ===============================================================




Custom TestCase assert messages
-------------------------------

The whole point of using the assert methods for TestCase is so that when an assertion fails, you get a detailed message that tells you what exactly caused the failure. The messages can be overwritten for any of the assert methods by providing a keyword ``msg`` to any of the assert methods (e.g. ``TestCase.assertEqual(a, b, msg="foo")``)


Showing custom messages and also assert output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If any assert methods are being overwritten by ``msg="foo"`` the old failure message can also be shown. Setting ``TestCase.longMessage=True`` during any test will show both custom failure messages and the original failure message.
