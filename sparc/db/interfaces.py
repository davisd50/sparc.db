from zope.interface import Interface
from zope import schema

class IQuery(Interface):
    """A database query"""
    query = schema.Text(
            title=_(u"A query to find events"),
            description=(u"Identifies the network address of the impacted host"),
            required = True
            )