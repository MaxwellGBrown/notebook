import pytest


@pytest.fixture(scope="session")
def session_fixture(request):
    print("session_fixture")
    def teardown_session_fixture():
        print("teardown_session_fixture")
    request.addfinalizer(teardown_session_fixture)

@pytest.fixture(scope="module")
def module_fixture(request):
    print("module_fixture")
    def teardown_module_fixture():
        print("teardown_module_fixture")
    request.addfinalizer(teardown_module_fixture)

@pytest.fixture(scope="class")
def class_fixture(request):
    print("class_fixture")
    def teardown_class_fixture():
        print("teardown_class_fixture")
    request.addfinalizer(teardown_class_fixture)

@pytest.fixture(scope="function")
def function_fixture(request):
    print("function fixture")
    def teardown_function_fixture():
        print("teardown_function_fixture")
    request.addfinalizer(teardown_function_fixture)

def setup_module(module):
    print("setup_module")

def teardown_module(module):
    print("teardown_module")


fixtures = [
            "session_fixture",
            "module_fixture",
            "class_fixture",
            "function_fixture",
           ]
@pytest.mark.usefixtures(*fixtures)
class TestThis(object):

    @classmethod
    def setup_class(cls):
        print("setup_class")

    @classmethod
    def teardown_class(cls):
        print("teardown_class")

    def setup_method(self, method):
        print("setup_method")

    def teardown_method(self, method):
        print("teardown_method")

    def test_this(request):
        assert True

    def test_that(request):
        assert True

    def test_wtf(request):
        assert True
