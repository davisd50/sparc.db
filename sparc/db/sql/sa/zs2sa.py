##############################################################################
#
# Copyright (c) 2008 Kapil Thangavelu <kapil.foss@gmail.com>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
Zope3 Schemas to SQLAlchemy

$Id: sa2zs.py 1710 2006-10-26 17:39:37Z hazmat $
"""
from zope import schema
import sqlalchemy as rdb

class FieldTranslator( object ):
    """ Translate a zope schema field to an sa  column
    """

    def __init__(self, column_type):
        self.column_type = column_type

    def extractInfo( self, field, info ):
        d = {}
        d['name'] = field.getName()
        if field.required:
            d['nullable'] = False
        d['default'] = field.default
        d['type'] = self.column_type        
        return d
    
    def __call__(self, field, annotation, primary_key=False):
        d = self.extractInfo( field, annotation )
        name, type = d['name'], d['type']
        del d['name']
        del d['type']
        return rdb.Column( name, type, primary_key=primary_key, **d)

class StringTranslator(FieldTranslator):
    
    column_type = rdb.Text

    def __init__(self, column_type=None):
        self.column_type = column_type or self.column_type
        
    def extractInfo( self, field, info ):
        d = super( StringTranslator, self ).extractInfo( field, info )
        if schema.interfaces.IMinMaxLen.providedBy( field ):
            d['type'].length = field.max_length
        return d

class ObjectTranslator(object):
    
    def __call__(self, field, metadata):
        table = transmute(field.schema, metadata)
        pk = get_pk_name(table.name)
        field_name = "%s.%s" % table.name, pk
        return rdb.Column(pk, rdb.Integer, rdb.ForeignKey(field_name),
            nullable=False)


fieldmap = {
    'ASCII': StringTranslator(),
    'ASCIILine': StringTranslator(),
    'Bool': FieldTranslator(rdb.BOOLEAN),
    'Bytes': FieldTranslator(rdb.BLOB),
    'BytesLine': FieldTranslator(rdb.BLOB),
    'Choice': StringTranslator(),
    'Date': FieldTranslator(rdb.DATE), 
    'Datetime': FieldTranslator(rdb.DATE), 
    'Decimal': FieldTranslator(rdb.Float), 
    'DottedName': StringTranslator(),
    'Float': FieldTranslator(rdb.Float), 
    'Id': StringTranslator(),
    'Int': FieldTranslator(rdb.Integer),
    'Object': ObjectTranslator(),
    'Password': StringTranslator(),
    'SourceText': StringTranslator(),
    'Text': StringTranslator(),
    'TextLine': StringTranslator(),
    'URI': StringTranslator(),
}

def transmute(zopeschema, metadata, tablename="", add_primary=True, key=None):

    columns = []

    for name, field in schema.getFieldsInOrder(zopeschema):
        classname = field.__class__.__name__
        translator = fieldmap[classname]
        if translator is None:
            print "Not translator found for %s" % classname
            continue
        primary_key = True if name == key else False
        columns.append(translator(field, metadata, primary_key=primary_key))

    if not tablename:
        tablename = zopeschema.getName()[1:]
        
    if add_primary:
        columns.insert(0, rdb.Column(get_pk_name(tablename), rdb.Integer,
                                     primary_key=True)
                       )

    return rdb.Table(tablename, metadata, *columns)

def get_pk_name(tablename):

    return "%s_id" % tablename.lower()

