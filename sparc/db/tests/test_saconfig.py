"""Test
"""
import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.db.tests

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('test_saconfig.txt',
                     package=sparc.db.tests),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')