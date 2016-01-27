import os
from importlib import import_module
from StringIO import StringIO
from zope.interface import alsoProvides
from sparc.db.splunk import ISplunkResultsStream

def mock_result_stream():
    """Return a ISplunkResultsStream from sample data"""
    response_file_path = os.path.join(import_module(__name__).__path__[0], 
                                      "splunk_job_result_stream_sample.xml")
    with open(response_file_path, 'r') as response_file:
        response = StringIO(response_file.read())
    alsoProvides(response, ISplunkResultsStream)
    return response