from zope.interface import Interface

class ISqlAlchemySession(Interface):
    """Marker for a session"""

class ISqlAlchemyDeclarativeBase(Interface):
    """Marker for a declarative base"""