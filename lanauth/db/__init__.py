"""
Database helper classes
"""
# Python stl imports
import contextlib
import logging

# External module imports
from sqlalchemy import Date, create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

# Globals
engine = None
Session = None

logger = logging.getLogger(__name__)


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    """Enables foreign key support on SQLite databases"""
    from sqlite3 import Connection as SQLite3Connection

    if isinstance(dbapi_connection, SQLite3Connection):
        print("Enabling ForeignKey support for SQLite3")
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def load_db(config=None):
    """
    Starts the database engine and loads a sessioni
    :param config:  SiteConfig object containing database settings
    """
    global engine, Session

    if config is not None:
        db_uri = config.get('database', 'uri', fallback="sqlite:///memory")
    else:
        db_uri = "sqlite:///memory"

    logger.info("Using database URI: %s" % db_uri)
    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine)

    # Build all tables
    from lanauth.db.models import Base
    Base.metadata.create_all(engine)


def to_dict(record):
    """
    Converts a database record into a dictionary
    :param record:  Database record
    :return:        Dictionary key=column value=value
    """
    rdict = {}
    for column in record.__table__.columns:
        value = getattr(record, column.name)

        # Convert datetime string
        print(type(column.type))
        if type(column.type) is Date:
            value = str(value)

        rdict[column.name] = value
            
    return rdict


@contextlib.contextmanager
def open_session():
    """
    Handles connections (sessions) with the database.
    """
    global engine, Session

    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
