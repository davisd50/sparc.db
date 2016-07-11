import os
import unittest
import zope.testrunner
from zope import component
from sparc.testing.fixture import test_suite_mixin
from sparc.testing.testlayer import SPARC_INTEGRATION_LAYER
from sparc.db.splunk.testing import SPARC_DB_SPLUNK_INTEGRATION_LAYER

from zope import schema
from zope.interface import Interface
class ITestSchema(Interface):
    date = schema.Date(title=u"date")
    datetime = schema.Datetime(title=u"datetime")
    decimal = schema.Decimal(title=u"decimal")
    float = schema.Float(title=u"float")
    int = schema.Int(title=u"int")
    bool = schema.Bool(title=u"bool")
    list = schema.Set(title=u"list", value_type=schema.Field(title=u"field"))
    set = schema.Set(title=u"set", value_type=schema.Field(title=u"field"))
    dict = schema.Dict(title=u"dict", key_type=schema.TextLine(title=u"key"),
                                value_type=schema.Text(title=u"value"))
    ip = schema.DottedName(title=u"ip",min_dots=3,max_dots=3)
    ascii = schema.ASCII(title=u"ascii")
            
class SparcCacheSplunkAreaTestCase(unittest.TestCase):
    layer = SPARC_INTEGRATION_LAYER
    sm = component.getSiteManager()
    
    def test_ISplunkKVCollectionSchema_adapter_for_schemas(self):
        from sparc.db.splunk import ISplunkKVCollectionSchema
        schema = ISplunkKVCollectionSchema(ITestSchema)
        
        self.assertIn('field.date', schema)
        self.assertEquals(schema['field.date'], 'time')
        
        self.assertIn('field.datetime', schema)
        self.assertEquals(schema['field.datetime'], 'time')
        
        self.assertIn('field.decimal', schema)
        self.assertEquals(schema['field.decimal'], 'number')
        
        self.assertIn('field.float', schema)
        self.assertEquals(schema['field.float'], 'number')
        
        self.assertIn('field.int', schema)
        self.assertEquals(schema['field.int'], 'number')
        
        self.assertIn('field.bool', schema)
        self.assertEquals(schema['field.bool'], 'bool')
        
        self.assertIn('field.list', schema)
        self.assertEquals(schema['field.list'], 'array')
        
        self.assertIn('field.set', schema)
        self.assertEquals(schema['field.set'], 'array')
        
        self.assertIn('field.dict', schema)
        self.assertEquals(schema['field.dict'], 'array')
        
        self.assertIn('field.ip', schema)
        self.assertEquals(schema['field.ip'], 'cidr')
        
        self.assertIn('field.ascii', schema)
        self.assertEquals(schema['field.ascii'], 'string')
        
    def test_bad_collection(self):
        from sparc.db.splunk import ISplunkKVCollectionSchema
        class ITestSchemaDict(Interface):
            list = schema.List(title=u'bad',
                                       value_type=schema.Dict(title=u'bad'))
        sschema = ISplunkKVCollectionSchema(ITestSchemaDict)
        self.assertNotIn('field.list', sschema)
            
        class ITestSchemaCollection(Interface):
            list = schema.List(title=u'bad',
                                       value_type=schema.List(title=u'bad'))
        sschema = ISplunkKVCollectionSchema(ITestSchemaDict)
        self.assertNotIn('field.list', sschema)



kv_names = {}
kv_names['test_collection'] = {}
kv_names['test_collection']['field.id'] = "string"
kv_names['test_collection']['field.name'] = "string"
SPARC_DB_SPLUNK_INTEGRATION_LAYER.kv_names.update(kv_names)
class SparcDBSplunkKVTestCase(unittest.TestCase):
    layer = SPARC_DB_SPLUNK_INTEGRATION_LAYER
    level = 2
    sm = component.getSiteManager()
    
    def test_current_kv_names(self):
        from sparc.db.splunk.kvstore import current_kv_names
        req = component.createObject(u'sparc.utils.requests.request')
        req.req_kwargs['verify'] = False
        req.gooble_warnings = True
        self.assertIn('test_collection', \
                      current_kv_names(self.layer.sci,
                                       self.layer.kv_username,
                                       self.layer.kv_appname,
                                       request=req))   

    def test_schema_adapter_for_named_collection(self):
        # tests SplunkKVCollectionSchemaFromSplunkInstance
        from sparc.db.splunk import ISplunkKVCollectionSchema
        from sparc.utils.requests import IRequest
        kv_id = self.layer.get_kv_id(u'test_collection')
        schema = component.getMultiAdapter((self.layer.sci, 
                                            kv_id,
                                            self.sm.getUtility(IRequest)), 
                                                ISplunkKVCollectionSchema)
        for k in self.layer.kv_names['test_collection'].keys():
            self.assertEquals(self.layer.kv_names['test_collection'][k], schema[k])

class test_suite(test_suite_mixin):
    package = 'sparc.db.splunk'
    module = 'kvstore'
    
    def __new__(cls):
        suite = super(test_suite, cls).__new__(cls)
        suite.addTest(unittest.makeSuite(SparcCacheSplunkAreaTestCase))
        suite.addTest(unittest.makeSuite(SparcDBSplunkKVTestCase))
        return suite


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])