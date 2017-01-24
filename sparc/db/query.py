from zope.component import createObject
from zope.component.factory import Factory
from zope import interface
from zope.schema import ValidationError
from zope.schema.fieldproperty import FieldProperty
from sparc.event import SparcEvent
from .interfaces import IQuery
from .interfaces import IQueryEvent
from .interfaces import IQueryResultSet
from .interfaces import IResultValue
from .interfaces import IResultMultiValue

@interface.implementer(IQuery)
class DbQuery(object):
    """A database query"""
    
    def __init__(self, query):
        self.query = query
    
    #IQuery
    query = FieldProperty(IQuery['query'])
dbQueryFactory = Factory(DbQuery)

@interface.implementer(IResultValue)
class ResultValue(str):
    """A value from a database query result (i.e. a table cell)"""
    
    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)
resultValueFactory = Factory(ResultValue)

@interface.implementer(IResultMultiValue)
class ResultMultiValue(object):
    """A value from a database query result that allows for multi-value fields"""
    
    def __init__(self, context):
        self.context = context
    
    def __repr__(self):
        return repr(self.context)
    
    #IResultMultiValue
    def __iter__(self):
        """Iterator of unicode capable ordered values"""
        return iter([createObject(u'sparc.db.result_value', value) for 
                                                        value in self.context])
resultMultiValueFactory = Factory(ResultMultiValue)

@interface.implementer(IQueryEvent)
class QueryEvent(SparcEvent):
    """A point-in-time executed query with results"""
    
    def __init__(self, **kwargs):
        """Object init
        
        Kwargs:
            [see sparc.event.event.SparcEvent]
            query: IQuery object
            results: IQueryResultSet object
        """
        super(QueryEvent, self).__init__(**kwargs)
        self.query = kwargs['query'].query
        if not IQueryResultSet.providedBy(kwargs['results']):
            raise ValidationError('expected IQueryResultSet for results, got: {}'.format("'" + str(kwargs['results']) + "'"))
        self.results = kwargs['results']

    #IQuery
    query =  FieldProperty(IQuery['query'])
    
    #IQueryResultSet
    def __iter__(self):
        return iter(self.results)
queryEventFactory = Factory(QueryEvent)