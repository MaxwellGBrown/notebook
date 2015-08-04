=====================
Pyramid & Nosetests
=====================

``pyramid`` was structured to cooperate with ``nose``. We can define our own test cases very easily using the same ``unittest`` library that ``nose`` leverages.

testing/app_example/tests.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import unittest

    from pyramid import testing


    class AppExampleViewTests(unittest.TestCase):
        # tests the controller output
        def setUp(self):
            self.config = testing.setUp()

        def tearDown(self):
            testing.tearDown()

        def test_home(self):
            
            request = testing.DummyRequest()
            response = home(request)
            self.assertEqual('Hello', response['title'])

    class AppExampleFunctionalTests(unittest.TestCase):
        # tests the rendered template
        def setUp(self):
            from app_example.setup_app import main
            app = main({})
            from webtest import TestApp

            self.testapp = TestApp(app)

        def test_home(self):
            response = self.testapp.get('/', status=200)
            self.assertIn(b'<h1>Hello World</h1>', response.body)


There are a few interesting things to note in our ``tests.py`` file:

1. The test file has a separate test class for the controllers (called ``view`` in pyramid), and the view (again, this view referring to the model-view-controller view, not ``pyramid.view``). This way the rendered template and the controller can be tested separately. This is a *Good Thing*.

2. The tests import ``pyramid.testing`` which is used to ``setUp`` and ``tearDown`` the application. ``testing.setUp`` will handle building the configuration for this application in the view tests. The application also uses ``testing.DummyRequest()`` to send a fake request for testing.

3. The tests use ``unittest.TestCase`` class methods to do all of our ``assert`` statements. This is done so that failed tests will show the comparison values instead of just showing that the comparison failed.

4. ``webtest.TestApp`` is imported in the functional tests. This separate package is used to create a wrapper for our application which we can send fake requests to and get the rendered templates and HTML response headers. 

what to write tests for
#######################

Tests can be written for literally everything on the planet. But the more tests that exist, the less malleable the actual code of the progam is. Tests should be created for end functionality that is to be preserved. Don't so much test for the steps along the way (unless, that is, it is a long and meticulous process). 

Also, the desired result should not be a super-exact set of requirements. Tests should check for the important sections and outcomes.

