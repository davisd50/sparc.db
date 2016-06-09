from zope.component import adapts
from zope.component.factory import Factory
from zope.interface import implements
from zope.interface import Interface
from zope.schema.interfaces import IField
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IBool
from zope.schema.interfaces import IDate, IDatetime
from zope.schema.interfaces import IDecimal, IFloat, IInt
from zope.schema.interfaces import IDict
from zope.schema.interfaces import IDottedName
from zope.schema.interfaces import IText, INativeString
from interfaces import ISplunkKVCollectionSchema

class SplunkKVCollectionSchema(dict):
    implements(ISplunkKVCollectionSchema)
splunkKVCollectionSchemaFactory = Factory(SplunkKVCollectionSchema)

# In the future, we may want to improve the usability of this adapter by
# providing Splunk KV specific markers to help identify override default field
# conversion behavior.
class SplunkKVCollectionSchemaFromZopeSchema(dict):
    implements(ISplunkKVCollectionSchema)
    adapts(Interface)
    
    def __init__(self, context):
        self.context = context
        super(SplunkKVCollectionSchemaFromZopeSchema, self).__init__()
        schema = self.get_collection_schema_from_interface_schema(context)
        for name in schema:
            self[name] = schema[name]

    @classmethod
    def get_collection_schema_from_interface_schema(self, schema):
        collection = {}
        for name in schema:
            if IDate.providedBy(schema[name]) or \
                                                IDatetime.providedBy(schema[name]):
                collection['field.'+name] = 'time'
            elif IDecimal.providedBy(schema[name]) or \
                                IFloat.providedBy(schema[name]) or \
                                               IInt.providedBy(schema[name]):
                collection['field.'+name] = 'number'
            elif IBool.providedBy(schema[name]):
                collection['field.'+name] = 'bool'
            elif ICollection.providedBy(schema[name]):
                if not ICollection.providedBy(schema[name].value_type) and not \
                            IDict.providedBy(schema[name].value_type):
                    collection['field.'+name] = 'array'
            elif IDict.providedBy(schema[name]):
                if IText.providedBy(schema[name].key_type) and \
                            IText.providedBy(schema[name].value_type):
                    collection['field.'+name] = 'array'
            # this is a pretty weak check for a IP address field.  We might want
            # to update this to look for a field validator based on the ipaddress package
            # or mark this field with a special interface indicating it is an 
            # IP address
            elif IDottedName.providedBy(schema[name]) and \
                            (schema[name].min_dots == schema[name].max_dots == 3):
                collection['field.'+name] = 'cidr'
            elif IText.providedBy(schema[name]) or \
                                        INativeString.providedBy(schema[name]):
                collection['field.'+name] = 'string'
        return collection