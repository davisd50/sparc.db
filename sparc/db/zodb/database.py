from ZODB import config
from zope.component import createObject
from zope.component import getUtility
from zope.component.factory import Factory
from zope.interface import alsoProvides
from zope.interface import implements
from interfaces import IZODBDatabase
from sparc.configuration.xml import IAppElementTreeConfig

class zodbDatabaseFactoryHelper(object):
    implements(IZODBDatabase)
    
    def __new__(self, *args, **kwargs):
        db = None
        if 'string' in kwargs:
            db = config.databaseFromString(kwargs['string'])
        if 'file' in kwargs:
            db = config.databaseFromFile(kwargs['file'])
        if 'url' in kwargs:
            db = config.databaseFromURL(kwargs['url'])
        if not db:
            raise ValueError('unable to obtain ZODB object from arguments')
        alsoProvides(db, IZODBDatabase)
        return db
zodbDatabaseFactory = Factory(zodbDatabaseFactoryHelper)

class zodbDatabaseFromConfigHelper(object):
    config_map = {} # {url: IZODBDatabase}
    
    def __new__(self, xml_config = None):
        url = None
        if xml_config is None or not len(xml_config):
            xml_config = getUtility(IAppElementTreeConfig)
        for sparc in xml_config.findall('sparc'):
            for db in sparc.findall('db'):
                for zodb in db.findall('zodb'):
                    url = zodb.attrib['url']
        if not url:
            raise LookupError('unable to find configuration for sparc::db::zodb::url')
        if url not in zodbDatabaseFromConfigHelper.config_map:
            db = createObject(u'sparc.db.zodb.database', url=url)
            zodbDatabaseFromConfigHelper.config_map[url] = db
        return zodbDatabaseFromConfigHelper.config_map[url]
zodbFromConfigFactory = Factory(zodbDatabaseFromConfigHelper)