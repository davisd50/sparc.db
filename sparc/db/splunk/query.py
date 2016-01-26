from zope.component.factory import Factory
from zope.interface import implements
from sparc.db.query import DbQuery
from sparc.db.splunk import ISplunkQuery

class SplunkQuery(DbQuery):
    implements(ISplunkQuery)

splunkQueryFactory = Factory(SplunkQuery)