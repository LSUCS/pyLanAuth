"""
SQL table models
"""
import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from lanauth.db import engine

Base = declarative_base(bind=engine)


class Authentications(Base):
    """
    Store a list of all sucessful authentications
    """
    __tablename__ = 'authentications'

    id         = Column(Integer, primary_key=True)  #: Unique identifier
    ip_addr    = Column(String(15))                 #: IP address
    lan        = Column(Float)                      #: Lan number
    username   = Column(String(64))                 #: Forums username
    seat       = Column(String(4))                  #: Seat at LAN
    status     = Column(Boolean, nullable=False)
    created_at = Column(DateTime)                   #: Creation timestamp of this record
    updated_at = Column(DateTime)                   #: Date the record was modified

    def __init__(self, ip_addr, lan, username, seat):
        self.ip_addr = ip_addr
        self.lan = lan
        self.username = username
        self.seat = seat
        self.status = False
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def __repr__(self):
        return "<Authentication(%s, %d, %s, %s)>" % (self.ip_addr, self.lan, self.username, self.seat)

    @staticmethod
    def add(session, ip_addr, lan, username, seat):
        """Add an authentication entry"""
        auth = Authentications(ip_addr, lan, username, seat)
        session.add(auth)
        session.flush()
        return auth


class AuthQueue(Base):
    """
    Stores a list of authentications that haven't been authenticated yet
    """
    __tablename__ = 'auth_queue'

    id      = Column(Integer, primary_key=True)         #: Unique identifier
    auth_id = Column(ForeignKey('authentications.id'))  #: Authentication entry

    auth = relationship('Authentications', backref="auth_queue")

    def __init__(self, auth):
        self.auth_id = auth.id
    

