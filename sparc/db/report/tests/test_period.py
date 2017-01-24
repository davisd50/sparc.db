import os
import zope.testrunner
from sparc.testing.fixture import test_suite_mixin
from sparc.db.testing import SPARC_DB_INTEGRATION_LAYER

class test_suite(test_suite_mixin):
    layer = SPARC_DB_INTEGRATION_LAYER
    package = 'sparc.db.report'
    module = 'period'


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])