from zope.component import adapts
from zope.component.factory import Factory
from zope.interface import implements
from sparc.db import IQueryResultSet
from sparc.db.query import DbQuery
from sparc.db.splunk import ISplunkQuery

class SplunkQuery(DbQuery):
    implements(ISplunkQuery)

splunkQueryFactory = Factory(SplunkQuery)

class QueryResultSetForSplunk(object):
    """A database query with results"""
    implements(IQueryResultSet)
    
    def __iter__():
        """Iterator of IResult objects"""