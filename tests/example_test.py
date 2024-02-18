'''# An example test to make sure the Pytest runner doesn't fail'''

import unittest

class ExampleTest(unittest.TestCase):
    '''# Example test class'''
    def test_example(self):
        '''# Example method'''
        self.assertEqual(1, 1)
