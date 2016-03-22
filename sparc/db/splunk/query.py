from splunklib.results import ResultsReader
from zope.component import adapts
from zope.component import createObject
from zope.component.factory import Factory
from zope.interface import alsoProvides
from zope.interface import implements
from sparc.db import IQueryResultSet
from sparc.db import ITabularResult
from sparc.db.query import DbQuery
from sparc.db.splunk import ISplunkQuery
from sparc.db.splunk import ISplunkResultsStream

class SplunkQuery(DbQuery):
    implements(ISplunkQuery)

splunkQueryFactory = Factory(SplunkQuery)

class QueryResultSetForSplunk(object):
    """A database query with results"""
    implements(IQueryResultSet)
    adapts(ISplunkResultsStream)
    
    def __init__(self, context):
        self.context = context

    def __iter__(self):
        """Iterator of IResult objects"""
        _seq = []
        for ordered_dict in ResultsReader(self.context):
            for key, value in ordered_dict.iteritems():
                if isinstance(value, basestring):
                    ordered_dict[key] = createObject(u'sparc.db.result_value', value)
                else:
                    ordered_dict[key] = createObject(u'sparc.db.result_multi_value', value)
            alsoProvides(ordered_dict, ITabularResult)
            _seq.append(ordered_dict)
        return iter(_seq)

