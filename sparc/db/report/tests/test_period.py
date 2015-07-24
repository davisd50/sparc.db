"""Test
"""
import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.db.report

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('period.txt',
                     package=sparc.db.report),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')