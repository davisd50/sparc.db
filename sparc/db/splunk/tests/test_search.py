"""Test
"""
import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.db.splunk

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('search.txt',
                     package=sparc.db.splunk),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')