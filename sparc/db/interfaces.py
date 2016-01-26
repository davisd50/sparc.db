from zope.interface import Interface
from zope import schema
from sparc.event import IEvent

from sparc.db import MessageFactory as _

#DB Query String
class IQuery(Interface):
    """A database query"""
    query = schema.Text(
            title=_(u"A query to find events"),
            description=(u"Identifies the network address of the impacted host"),
            required = True
            )

#DB Query Results
class IQueryResultSet(IQuery):
    """A database query with results"""
    def __iter__():
        """Iterator of IResult objects"""

class IResult(Interface):
    """A single database query result (i.e. a row)"""

class ITabularResult(IResult):
    """A single database query result represented as a Python dictionary whose
    key values are instances of ITabularResultMultiValue or ITabularResultValue

    Sample implementation:
        >>> from zope.interface import implements
        >>> class MyColumnarResult(dict):
        ...     implements(IColumnarResult)
    """

#DB Query Result Values
class ITabularResultValue(Interface):
    """A value from a database query result (i.e. a table cell)"""
    def __unicode__():
        """Return unicode string representation of value"""

class ITabularResultMultiValue(Interface):
    """A value for a ITabularResult key that allows for multi-value fields"""
    def __iter__():
        """Iterator of unicode capable values"""

#DB Query Event
class IQueryEvent(IEvent, IQueryResultSet):
    """A point-in-time executed query with results"""
