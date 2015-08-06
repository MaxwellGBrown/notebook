from unittest import TestCase


class BasicTests(TestCase):
    status = "Not Testing"

    def setUp(self):
        self.status = "Testing"

    def tearDown(self):
        self.status = "Not Testing"

    def test_setUp_runs_at_start(self):
        self.assertEqual(self.status, "Testing")
