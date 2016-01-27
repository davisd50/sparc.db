from zope.interface import Interface
from sparc.db import IQuery

class ISplunkQuery(IQuery):
    """A Splunk query"""

class ISplunkResultsStream(Interface):
    """A Splunk job results stream handle"""
    def read():
        """Reads stream and advances pointer"""

class ISplunkSavedSearches(Interface):
    """Marker for splunklib.client.SavedSearches"""

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