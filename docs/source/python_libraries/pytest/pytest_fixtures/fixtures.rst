.. _pytest_fixtures:

===============
pytest fixtures
===============

pytest differs from other unit testing packages in the way it handles fixtures. 

The basic doc on setting up fixtures can be found `here <http://pytest.org/latest/fixture.html>`_.

Fixtures are used to create (and tear down) a testing environment that are separate from the things being tested. There are several ways to operate with them:

#. Passing fixtures as function arguments of the same name (aka *black magic*)
#. Passing fixtures as strings of the same name to the wrapper ``pytest.mark.usefixtures`` (explicit > implicit)
#. Setting up xunit style setup/teardown class methods (most explicit, least flexible)

.. code-block:: python

  import pytest

  @pytest.fixture
  def foo():
      class Foo(object):
          bar = "Hello World"
      return Foo


  # fixture as function argument of the same name
  def test_foobar(foo):
      assert foo.bar == "Hello World"


  # fixture as wrapper: assess fixtures using pytest request object
  @pytest.mark.usefixtures("foo")
  def test_using_fixture_foo(request):
     foo = request._funcargs['foo']
     assert foo.bar == "Hello World"


  # xunit setup/teardown fixtures 
  class TestXunitFixture(object):

      def setup_method(self, method):
          self.bar = "Hello World"

      def test_xunit_setup(self):
          assert self.bar == "Hello World"


-------------
Fixture Scope
-------------

Defining the module/class/method scope for fixtures isn't exclusive to the
XUnit style fixtures; this concept is preserved across all pytest fixtures. 

In fact, the xunit setup/teardowns work separately from pytest fixtures so a class can leverage both.

To declare a scope other than the default function scope, declare the keyword
argument ``scope`` to the desired scope to these scopes:

Scope declaration also allows the ability to "teardown" fixtures, which is done by calling ``request.addfinalizer()`` on the fixture's pytest request.

Below is a light example of setting this up:

.. code-block:: python

  import pytest

  @pytest.fixture(scope="class")
  def class_fixture(request):
      # setUp

      def teardown_class_fixture():
          pass  # tearDown
      request.add_finalizer(teardown_class_fixture)


  class TestSuite(object):

      @classmethod
      def teardown_class(cls):
          pass

      def setup_method(self, method):
          pass

      def test_this(self, request):
          assert True


The available operatable scopes are:

* session - shared across all tests & modules in this py.test run
* module - shared in all tests within the same module
* class - shared in all tests within the same class
* function/module - used only by this one test

In the scope of things, fixtures are always set up before the xunit ``setup``
functions:: 

  session_fixture
    setup_module
      module_fixture
        setup_class
          class_fixture
            setup_method
              function fixture
                TEST
              teardown_function_fixture
            teardown_method
          teardown_class_fixture
        teardown_class
      teardown_module_fixture
    teardown_module
  teardown_session_fixture

To run this scope example, use :download:`this file<./fixture_scope.py>` and from the
command line ``$ py.test -v -s``.

.. note::

   This is a representation of how things *should* work, but the setup_* xunit
   callables are run independently from the test fixtures. It's important to
   *avoid relying on fixtures in xunit setups/teardowns* and they should remain
   separate.


.. _pytest_nested_fixtures:

----------------
Nesting Fixtures
----------------

Fixtures that rely on other fixture's setup can use those other fixtures as
arguments just like test cases take fixtures as arguments.

.. code-block:: python

    import pytest

    @pytest.fixture
    def fixture1(request):
        fixture_list = list(['fixture1'])
        return fixture_list

    @pytest.fixture
    def fixture2(fixture1):
        new_fixture_list = list(fixture1)
        new_fixture_list.append("fixture2")
        return new_fixture_list

    @pytest.fixture
    def fixture3(fixture2):
        new_fixture_list = list(fixture2)
        new_fixture_list.append("fixture3")
        return new_fixture_list

    @pytest.mark.usefixtures("fixture3")  # only fixture3 is supplied!
    def test_nested_fixtures(request):
        # also contains fixture2 & fixture1!
        fixture3_list = request._funcargs['fixture3']
        assert "fixture1" in fixture3_list
        assert "fixture2" in fixture3_list
        assert "fixture3" in fixture3_list


For a full in-depth example of this, :download:`check out this file<./nested_fixtures.py>`.

.. note::

   While it's possible to nest fixtures using ``@pytest.mark.usefixtures``, to 
   have it operate correctly *all* of it's nested fixtures must be supplied to 
   the test case that relies on that fixture tree, somewhat defeating the
   purpose.

   This is *sad* for my disdain of py.test's black-magic arg-fixture name
   matching.


----------------------
Parameterized Fixtures
----------------------

A fixture can be set up to run with different parameters, so that a new test
will be created for each supplied parameter.

This can also be set up at the test_case scope, but is sometimes more
appropriate for the fixture scope.

.. code-block:: python

    @pytest.fixture(params=["param1", "param2", "param3"])
    def param_fixture(request):
        return request.param


    @pytest.mark.usefixture("param_fixture")
    def test_param_fixture(request):
        print(request._funcargs['param_fixture'])
        assert True
