from zope.interface import Interface
from zope import schema
from sparc.db import IQuery

class ISplunkQuery(IQuery):
    """A Splunk query"""

class ISplunkResultsStream(Interface):
    """A Splunk job results stream handle"""
    def read():
        """Reads stream and advances pointer"""

class ISplunkJob(Interface):
    """Marker for splunklib.client.Job"""

class ISplunkSavedSearches(Interface):
    """Marker for splunklib.client.SavedSearches"""

class ISplunkSavedSearch(Interface):
    """Marker for splunklib.client.SavedSearch"""

class ISplunkSavedSearchIterator(Interface):
    """Iterator of ISplunkSavedSearch providers"""
    def __iter__():
        """returns iterator of ISplunkSavedSearch providers"""

class ISplunkConnectionInfo(Interface):
    """A Python dict for Splunk connection info. see splunklib.client.connect
    
    Implementers should make sure these objects can be passed into such as
    splunklib.client.connect(**implementation)
    
    Sample implementation:
        >>> from zope.interface import implements
        >>> class MySplunkConnInfo(dict):
        ...     implements(ISplunkConnectionInfo)
    """

class ISplunkSavedSearchQueryFilter(Interface):
    """A Python str for a regex Splunk Saved Search name filer
    
    Sample implementation:
        >>> from zope.interface import implements
        >>> class MySplunkSavedSearchQueryFilter(str):
        ...     implements(ISplunkSavedSearchQueryFilter)
        
    """

class ISplunkKVCollectionSchema(Interface):
    """A Dict-based Splunk KV Collection schema definition
    
    This should be a Python dict whose keys are strings that define Splunk
    KV collection field names and values define that fields Splunk data type.
    Other non-attribute fields may be defined as well in the same manor (such
    as accelerated_fields, etc).
    
    
    Sample implementation:
        >>> from zope.interface import implements
        >>> class MySplunkKVSchema(dict):
        ...     implements(ISplunkKVCollectionSchema)
    """

class ISPlunkKVCollectionIdentifier(Interface):
    """An identifier for a Splunk KV Collection end point"""
    collection = schema.TextLine(title=u"Collection Name")
    application = schema.TextLine(title=u"Splunk Application Name")
    username = schema.TextLine(title=u"Splunk Associated User Name")