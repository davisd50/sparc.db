from interfaces import ISplunkConnectionInfo
from interfaces import ISplunkQuery
from interfaces import ISplunkResultsStream
from interfaces import ISplunkJob
from interfaces import ISPlunkKVCollectionIdentifier
from interfaces import ISplunkKVCollectionSchema
from interfaces import ISplunkSavedSearch
from interfaces import ISplunkSavedSearches
from interfaces import ISplunkSavedSearchQueryFilter

# XML name spaces for REST API ElementTree searching
xml_ns = {
          'atom': 'http://www.w3.org/2005/Atom',
          's': 'http://dev.splunk.com/ns/rest',
          'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'
        }