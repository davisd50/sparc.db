import warnings
import xml.etree.ElementTree as ET
from zope import component
from sparc.testing.testlayer import SparcZCMLFileLayer
import sparc.testing

from sparc.utils.requests.request import Request
from kvstore import current_kv_names


class SparcDBSplunkLayer(SparcZCMLFileLayer, Request):
    
    """Tuple of KV collection definitions.
    
    This should be initialized by tests.  This is a 2-dimensional dictionary.  
    The outer dictionary key should be the kv collection name.  The value of 
    this dict should be another dict describing the collection schema.  All
    field name keys need to have 'field.' prefix per Splunk schema naming
    standards
    """
    kv_names = {}
    
    kv_username = u'nobody' # 'nobody' is typical to let all users see the KV collection
    kv_appname = u'search'
    
    @property
    def sci(cls):
        sci = component.createObject(
                            u"sparc.db.splunk.splunk_connection_info_factory")
        sci['host'] = 'splunk_testing_host' # NOT PROD HOST!!!!!...easiest to set this in your host file
        sci['port'] = '8089'
        sci['username'] = 'admin'
        sci['password'] = 'admin'
        return sci
    
    @property
    def url(self):
        sci = self.sci
        return 'https://'+sci['host']+':'+sci['port']+'/servicesNS/' \
                                    +self.kv_username+'/'+self.kv_appname+'/'
    
    @property
    def auth(self):
        return (self.sci['username'], self.sci['password'], )
    
    def get_current_kv_names(self):
        """Return String names of current available Splunk KV collections"""
        return current_kv_names(self.sci, self.kv_username, self.kv_appname, request=self)
    
    def get_kv_id(self, collection):
        return component.createObject(\
                            u"sparc.db.splunk.kv_collection_identifier",
                            collection=collection,
                            application=self.kv_appname,
                            username=self.kv_username)
    
    def _destroy_kv_collections(self):
        for name in [n for n in self.kv_names if n in self.get_current_kv_names()]:
            r = self.request('delete', self.url+"storage/collections/config/"+name)
            r.raise_for_status()
        names = self.get_current_kv_names()
        for name in self.kv_names:
            if name in names:
                raise EnvironmentError('unexpectedly found %s in kv collections %s' % (name, str(self.kv_names.keys())))
    
    def _create_kv_collections(self):
        for name in self.kv_names:
            if name not in self.get_current_kv_names():
                r = self.request('post',self.url+"storage/collections/config",
                                    headers = {'Content-Type': 'application/json'},
                                    data={'name': name})
                r.raise_for_status()
            r = self.request('post',self.url+"storage/collections/config/"+name,
                                headers = {'Content-Type': 'application/json'},
                                data=self.kv_names[name])
            r.raise_for_status()
            if name not in self.get_current_kv_names():
                raise EnvironmentError('expected %s in list of kv collections %s' % (name, str(self.get_current_kv_names())))
    
    def setUp(self):
        super(SparcDBSplunkLayer, self).setUp()
        self.req_kwargs['verify'] = False
        self.req_kwargs['auth'] = self.auth
        self.gooble_warnings = True
        self._destroy_kv_collections()
        self._create_kv_collections()
        warnings.warn("This test layer requires a running Splunk instance.  See %s for connection information." % __file__)

    def tearDown(self):
        with warnings.catch_warnings():
            self._destroy_kv_collections()
            warnings.simplefilter("ignore") # ignore https cert warnings
        super(SparcDBSplunkLayer,self).tearDown()

SPARC_DB_SPLUNK_INTEGRATION_LAYER = SparcDBSplunkLayer(sparc.testing) #should initialize the ftesting.zcml file
