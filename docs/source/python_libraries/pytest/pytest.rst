.. _pytest:

======
pytest
======

pytest is a unit-testing framework. Use it to write & run unit tests.

**Examples**

.. toctree::
  :maxdepth: 2

  Fixtures <pytest_fixtures/fixtures>


----------
Quickstart
----------

To start w/ pytest, first write a test! Pytest has pretty good test discovery. The best way to ensure tests are discovered is by prefixing them with ``test_``

.. code-block:: python

  def test_this():
      assert True


To run tests, head to the command line and enter::

  $ py.test

It's that easy!


Logically it may make sense to group tests into classes. pytest is totally down with this.

.. code-block:: python

  class TestThese(object):
  
      this = "Foo"
      that = "Bar"

      def test_foo(self):
          assert self.this == "Foo" 

      def test_bar(self):
          assert self.that == "Bar"


Really there's much much more to working with pytest, but this here is the it at it's most basic.

For more in-depth, look into :ref:`defining fixtures <pytest_fixtures>`
