from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()

class User(Base):
    """ User model """
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(250), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    urls = relationship('Url', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User(username={self.username}, email={self.email})>'


class Url(Base):
    """ Urls model """
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(250), nullable=False)
    short_url = Column(String(100))
    user_id = Column(String(50), ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow())

    user = relationship(User, back_populates='urls')
    visits = relationship('Visit', backref='url', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Url(url={self.url}, short_url={self.short_url})>'


class Visit(Base):
    """ Visits/clicks model """
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(20))
    timestamp = Column(DateTime, default=datetime.utcnow())
    url_id = Column(Integer, ForeignKey('urls.id'))

    def __repr__(self):
        return f'<Visit(ip_address={self.ip_address}, timestamp={self.timestamp})>'
