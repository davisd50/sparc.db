from sqlalchemy.ext.declarative import declarative_base, declared_attr

from sparc.db import ISqlAlchemySession

# Class to act as a Base for all ORM-based SQLAlchemy mappings
Base = declarative_base()

class sparcBaseMixin(object):
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}
    
    def __repr__(self):
        try:
            _id = self.getId()
        except KeyError:
            _id = None
        return "<" + self.__class__.__name__ + "(id: '%s')>" % (str(_id))

class EngineRequired(object):
    """Decorator for callables that are dependent on a SQLite SQLAlchemy engine
    
    Args:
        *args: String SQLAlchemy engine name that is required.  String must match
               a valid SQLAlchemy engine name (see engine.get_bind() method from
               SQLAlchemy...http://docs.sqlalchemy.org/en/rel_0_9/orm/session_api.html?highlight=get_bind#sqlalchemy.orm.session.Session.get_bind)
    
    Usage:
        Define a class that is decorated with EngineRequired().
        
        >>> from sparc.db import EngineRequired
        >>> @EngineRequired('sqlite','oracle')
        ... class myTestClass(object):
        ...     def __init__(self, aSessionArg):
        ...         self.session = aSessionArg
        
        Create a session, make sure it provides the sparc.db.ISqlAlchemySession 
        interface.  If your app is configured, and included configure.zcml 
        from sparc.db then this is already done, otherwise you'll need to do it
        yourself via zope.interface.directlyProvides().  We'll grab our ready-made
        session for this example that uses a sqlite memory-only db.
        
        >>> from sparc.common import Configure
        >>> import sparc.db
        >>> Configure([sparc.db, (sparc.db, 'memory.zcml')])
        >>> from z3c.saconfig import named_scoped_session
        >>> Session = named_scoped_session('memory_session')
        >>> session = Session()
        
        >>> from sparc.db import ISqlAlchemySession
        >>> ISqlAlchemySession.providedBy(session)
        True
        
        Now we'll test object instantiation.
        
        >>> myObject = myTestClass(session)
        >>> ISqlAlchemySession.providedBy(myObject.session)
        True
        
        Ok, now test another implementation that only uses oracle
        
        >>> @EngineRequired('oracle')
        ... class myFailingClass(object):
        ...     def __init__(self, aSessionArg):
        ...         self.session = aSessionArg
        
        
        >>> try:
        ...     myObject = myFailingClass(session)
        ... except LookupError:
        ...    print True
        True
        
    """
    def __init__(self, *args):
        self._allowed_engines = args
    
    def __call__(self, classThatRequiresSpecificEngine):
        def checkEngine(*args, **kwargs):
            session = None
            for a in args:
                if ISqlAlchemySession.providedBy(a):
                    session = a
                    break
            if not session:
                for a in kwargs.values():
                    if ISqlAlchemySession.providedBy(a):
                        session = a
                        break
            if not session:
                raise LookupError("expected class to be initialized with "\
                                  "ISqlAlchemySession argument (a SQLAlchemy session that provides the ISqlAlchemySession interface).")
            engine = session.get_bind()
            if engine.name not in self._allowed_engines:
                raise LookupError('Implementation requires SQLAlchemy engine of dialect %s, got: %s', str(self._allowed_engines), engine.name)
            return classThatRequiresSpecificEngine(*args, **kwargs)
        return checkEngine
