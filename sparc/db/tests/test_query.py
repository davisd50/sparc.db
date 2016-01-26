import unittest
from doctest import DocTestSuite
from doctest import DocFileSuite

import sparc.db

def test_suite():
    return unittest.TestSuite((
        DocFileSuite('query.txt',
                     package=sparc.db),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')