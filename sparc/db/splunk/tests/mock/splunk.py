"""
We need these mock components in order to provide test coverage in the absense
of a testing Splunk instance.
"""
from zope.component import getGlobalSiteManager
from zope.component import IFactory
from zope.component.factory import Factory
import penny.apps.reaper.splunk.search

from splunklib.client import Service
from splunklib.client import SavedSearch
from splunklib.client import SavedSearches

search_list = []

class MockSavedSearch(SavedSearch):
    """A mock saved search"""

class MockSavedSearches(SavedSearches):
    """A mock saved search collection"""
    def iter(self, **kwargs):
        for entry in search_list:
            yield MockSavedSearch(**entry)

def mock_saved_searches_factory_helper(**splunk_connection_info):
    """Return a splunklib.client.SavedSearches object marked with 
       ISplunkSavedSearches
    """

mock_saved_searches_factory = Factory(mock_saved_searches_factory_helper,
                                 u'penny.apps.reaper.saved_searches_factory',
                                 u'Creates instances of ISplunkSavedSearches')

def replace_saved_searches_factory_with_mocker():
    """Update the ZCA Global Registry with a mock replacement for 
       penny.apps.reaper.saved_searches_factory
    """
    gsm = getGlobalSiteManager()
    gsm.unregisterUtility(
            component=penny.apps.reaper.splunk.search.saved_searches_factory, 
            provided=IFactory, 
            name=u'penny.apps.reaper.saved_searches_factory')
    gsm.registerUtility(mock_saved_searches_factory, 
                        IFactory, 
                        u'penny.apps.reaper.saved_searches_factory')
