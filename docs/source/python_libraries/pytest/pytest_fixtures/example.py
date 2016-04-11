""" run from command line w/ $py.test """

import pytest


@pytest.fixture
def foo():
    class Foo(object):
        bar = "Hello World"
    return Foo

# fixture as function argument of the same name
def test_foobar(foo):
    assert foo.bar == "Hello World"

# fixture as wrapper: acces fixtures using ``request`` a generic pytest class
@pytest.mark.usefixtures("foo")
def test_using_fixture_foo(request):
    print(vars(request))
    foo = request._funcargs['foo']
    assert foo.bar == "Hello World"


class TestXunitFixture(object):

    def setup_method(self, method):
        self.bar = "Hello World"

    def test_xunit_setup(self):
        assert self.bar == "Hello World"
