from unittest import TestCase


class BasicTests(TestCase):
    status = "Not Testing"
    class_status = "Not Constructed"

    @classmethod
    def setUpClass(cls):
        cls.class_status = "Set Up"

    def setUp(self):
        if self.class_status != "Set Up":
            raise Exception("BasicTests was not \'Set Up\'!")
        self.status = "Testing"

    @classmethod
    def tearDownClass(cls):
        cls.class_status = "Torn Down"

    def tearDown(self):
        self.status = "Not Testing"

    def test_setUp_runs_at_start(self):
        """
        BasicTests is "Testing" while running unit tests
        """
        self.assertEqual(self.status, "Testing")
