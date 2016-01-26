sparc.db
========

Database interaction utilities for the SPARC platform.

SQL Databases
-------------
Interactions to SQL databases are provided via SQLAlchemy (http://www.sqlalchemy.org/).
In addition, z3c.saconfig (https://pypi.python.org/pypi/z3c.saconfig) is 
provided to allow connection configuration andintegration of SQLAlchemy in ZCA.

### Usage - SQLite memory DB connection
    These steps will give you access to a SQLAlchemy session, see the SQLAlchemy
    docs to understand how to interact with this object.
    >>> import sparc.db
    >>> from sparc.configuration.zcml import Configure
    >>> from zope.component import getUtility
    >>> from z3c.saconfig.interfaces import IEngineFactory, IScopedSession
    >>> Configure((sparc.db, 'memory.zcml',))
    >>> myEngine = getUtility(IEngineFactory, name="memory_engine")
    >>> mySession = getUtility(IScopedSession, name="memory_session")
    
    The above example gives access to a in-memoery SQLite instance.  In practice,
    you would create your own db.zcml with the appropriate connection information.
    See SAConfig documentation on how to create the ZCML configu file.