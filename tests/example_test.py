# An example test to make sure the Pytest runner doesn't fail

import unittest

class ExampleTest(unittest.TestCase):
    def test_example(self):
        self.assertEqual(1, 1)
