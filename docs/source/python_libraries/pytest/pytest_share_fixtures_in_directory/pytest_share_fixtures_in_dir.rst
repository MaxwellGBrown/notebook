=====================================================
Sharing Fixtures Across Modules in the Same Directory
=====================================================

Oftentimes, test cases in separate modules may rely on common fixtures.

However, simply declaring the scope of these fixtures as "session" isn't enough for them to be shared. In these scenarios, each module spins up a new "session" before tearing down the other one. This is an issue, say, if there's a fixture loading test data. The set of test data would be loaded in multiple times!

To alleviate this, the fixtures need to be grouped in a ``conftest.py`` file in that same directory.

--------------------------------------
Housing shared fixtures in conftest.py
--------------------------------------

It seems logical to group shared fixtures, say, in a file called ``tests/fixtures.py``.

::

  # content of tests/fixtures.py

  import pytest

  already_open = False
  @pytest.fixture(scope="session")
  def singleton_fixture(request):
      if already_open is True:
          raise Exception()

      global already_open
      already_open = True

      request.addfinalizer(lambda: already_open = False)


  # content of tests/test_a.py

  from tests.fixtures import singleton_fixture

  def test_a(singleton_fixture):
      assert True


  # content of tests/test_b.py

  from tests.fixtures import singleton_fixture

  def test_b(singleton_fixture):
      assert True


Surprisingly, ``test_b`` will fail w/ an Error, because ``singleton_fixture`` is constructed again before the end of the session, instead of being shared across ``test_a`` & ``test_b``.

The very simple solution to all this, is to store the fixtures in ``tests/conftest.py``!

::

  # content of tests/conftest.py

  import pytest

  already_open = False
  @pytest.fixture(scope="session")
  def singleton_fixture(request):
      if already_open is True:
          raise Exception()

      global already_open
      already_open = True

      request.addfinalizer(lambda: already_open = False)


  # content of tests/test_a.py

  def test_a(singleton_fixture):
      assert True


  # content of tests/test_b.py

  def test_b(singleton_fixture):
      assert True


This setup passes w/ flying colors, as now the ``singleton_fixture`` is shared on the session scope **like it was supposed to have been**.

Also notice that one doesn't have to import the fixtures to use them in the test cases anymore!
