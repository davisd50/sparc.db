"""Test pwsecurity.sc.cache.corp_3pc_tracker module.
"""
import unittest
from doctest import DocTestSuite

import logging, sys

def test_suite():
    return unittest.TestSuite((DocTestSuite('sparc.db.sql'),))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')