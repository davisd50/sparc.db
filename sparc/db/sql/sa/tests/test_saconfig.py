"""Test
"""
import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.db.sql.sa.tests

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('test_saconfig.txt',
                     package=sparc.db.sql.sa.tests),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')