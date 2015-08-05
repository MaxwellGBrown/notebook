import unittest

from pyramid import testing


class BasicAppControllerTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .views import BasicAppController

        request = testing.DummyRequest()
        controller = BasicAppController(request)
        response = self.controller.home()
        # Test the data sent to the template for rendering
        self.assertEqual('Home View', response['name'])

    def test_hello(self):
        from .views import AppExampleViews

        request = testing.DummyRequest()
        controller = BasicAppController(request)
        response = self.controller.hello()
        # Test the data sent to the template for rendering
        self.assertEqual('Hello View', response['name'])


class BasicAppFunctionalTests(unittest.TestCase):
    def setUp(self):
        from basic_app.setup_app import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        response = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hi Home View</h1>', response.body)

    def test_hello(self):
        response = self.testapp.get('/howdy', status=200)
        self.assertIn(b'<h1>Hi Hello View</h1>', response.body)
