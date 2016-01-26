from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from interfaces import IQuery

class DbQuery(object):
    """A database query"""
    implements(IQuery)
    
    def __init__(self, query):
        self.query = query
    
    #IQuery
    query = FieldProperty(IQuery['query'])

dbQueryFactory = Factory(DbQuery)