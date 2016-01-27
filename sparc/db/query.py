from zope.component import createObject
from zope.component.factory import Factory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from interfaces import IQuery
from interfaces import IResultValue
from interfaces import IResultMultiValue

class DbQuery(object):
    """A database query"""
    implements(IQuery)
    
    def __init__(self, query):
        self.query = query
    
    #IQuery
    query = FieldProperty(IQuery['query'])

dbQueryFactory = Factory(DbQuery)

class ResultValue(str):
    """A value from a database query result (i.e. a table cell)"""
    implements(IResultValue)
    
    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)

resultValueFactory = Factory(ResultValue)


class ResultMultiValue(object):
    """A value from a database query result that allows for multi-value fields"""
    implements(IResultMultiValue)
    
    def __init__(self, context):
        self.context = context
    
    def __repr__(self):
        return repr(self.context)
    
    #IResultMultiValue
    def __iter__(self):
        """Iterator of unicode capable ordered values"""
        for value in self.context:
            yield createObject(u'sparc.db.result_value', value)

resultMultiValueFactory = Factory(ResultMultiValue)