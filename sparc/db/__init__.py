# I18N messaging
from sparc.i18n import SparcMessageFactory
MessageFactory = SparcMessageFactory('sparc.db')

from .interfaces import IQuery
from .interfaces import IQueryEvent
from .interfaces import IQueryResultSet
from .interfaces import IResult
from .interfaces import ITabularResult
from .interfaces import IResultMultiValue
from .interfaces import IResultValue