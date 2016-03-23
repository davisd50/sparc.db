import os
import unittest
import zope.testrunner
import sparc.db.splunk as splnk
from zope import component
from zope import interface
from sparc.testing.fixture import test_suite_mixin
from sparc.testing.testlayer import SPARC_INTEGRATION_LAYER

# Splunk connection information
connect = {
           'host': 'splunk-pso.ec2.beta',
           'port': '8089',
           'username': 'pso_reaper1',
           'password': 'wkUwLzFjDGBZ'
           }


class SparcDbSplunkSearchTestCase(unittest.TestCase):
    level = 2
    layer = SPARC_INTEGRATION_LAYER
    sm = component.getSiteManager()
    
    def _get_connect_info(self, connect):
        connect_info = \
            component.createObject(\
                            u'sparc.db.splunk.splunk_connection_info_factory')
        connect_info.update(connect)
        return connect_info

    def test_connection_failure(self): 
        connect_info = self._get_connect_info(connect)
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