# I18N messaging
from sparc.i18n import SparcMessageFactory
MessageFactory = SparcMessageFactory('sparc.db')

# Configuration (this package only)
from importlib import import_module
from sparc.configuration.zcml import Configure as SparcConfigure
def Configure():
    SparcConfigure([import_module(__name__)])

from interfaces import IQuery
from interfaces import IQueryEvent
from interfaces import IQueryResultSet
from interfaces import IResult
from interfaces import ITabularResult
from interfaces import IResultMultiValue
from interfaces import IResultValue