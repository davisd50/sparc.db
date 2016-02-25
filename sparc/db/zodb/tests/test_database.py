"""Test
"""
import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.db.zodb

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('database.txt',
                     package=sparc.db.zodb),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')