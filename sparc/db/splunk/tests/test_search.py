import os
import unittest
import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from sparc.testing.testlayer import SPARC_INTEGRATION_LAYER

class SparcDbSplunkSearchTestCase(unittest.TestCase):
    level = 2
    layer = SPARC_INTEGRATION_LAYER
    sm = component.getSiteManager()

    def test_connection_failure(self):
        from sparc.db.splunk.tests import splunk_connection_info
        connect_info = self._get_connect_info(splunk_connection_info)
        connect_info['password'] = 'bad-password'
        
        from splunklib.binding import AuthenticationError
        
        with self.assertRaises(AuthenticationError):
            component.createObject(u'sparc.db.splunk.saved_searches_factory',
                                                                connect_info)

class test_suite(test_suite_mixin):
    package = 'sparc.db.splunk'
    module = 'search'
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcDbSplunkSearchTestCase))
        return suite


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])