from zope.interface import implements
from zope.interface.exceptions import DoesNotImplement
from zope.component.factory import Factory
from splunklib.client import connect
from interfaces import ISplunkConnectionInfo
from interfaces import ISplunkSavedSearchQueryFilter

from sparc.logging import logging
logger = logging.getLogger(__name__)

class SplunkConnectionInfo(dict):
    """A Python dict for Splunk connection info. see splunklib.client.connect"""
    implements(ISplunkConnectionInfo)
splunk_connection_info_factory = Factory(SplunkConnectionInfo,
                        u'penny.apps.reaper.splunk_connection_info_factory',
                        u'Creates instances of ISplunkConnectionInfo')

class SplunkSavedSearchQueryFilter(str):
    """A Python str for a regex Splunk Saved Search name filer"""
    implements(ISplunkSavedSearchQueryFilter)
splunk_saved_search_query_filter_factory = Factory(SplunkSavedSearchQueryFilter,
                u'penny.apps.reaper.splunk_saved_search_query_filter_factory',
                u'Creates instances of ISplunkSavedSearchQueryFilter')

def saved_searches_factory_helper(splunk_connection_info):
    """Return a valid splunklib.client.SavedSearches object
    
    kwargs:
        - see splunklib.client.connect()
    """
    if not ISplunkConnectionInfo.providedBy(splunk_connection_info):
        DoesNotImplement('argument did not provide expected interface')
    service = connect(**splunk_connection_info)
    saved_searches = service.saved_searches
    for s in saved_searches:
        logger.debug("Found Splunk saved search with name %s" % s.name)
    return saved_searches

saved_searches_factory = Factory(saved_searches_factory_helper,
                                 u'penny.apps.reaper.saved_searches_factory',
                                 u'Creates instances of ISplunkSavedSearches')