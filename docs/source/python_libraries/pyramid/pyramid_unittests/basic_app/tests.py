import unittest

from pyramid import testing


class AppExampleViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        from app_example.views import hello_world

        request = testing.DummyRequest()
        response = hello_world(request)
        # Test the data sent to the template for rendering
        self.assertEqual('Hello World', response['title'])


class AppExampleFunctionalTests(unittest.TestCase):
    def setUp(self):
        from app_example.setup_app import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_hello_world(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hello World</h1>', res.body)
