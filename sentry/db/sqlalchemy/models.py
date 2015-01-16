from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import object_mapper
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, DateTime, Boolean, Text, Index
from sqlalchemy import String, Integer

from sentry.openstack.common import jsonutils

BASE = declarative_base()


class BaseModel(object):
    """Base class for models."""

    __table_initialized__ = False

    _json_fields = []
    _sortable_excludes = []
    _searchable_excludes = []

    @classmethod
    def get_fields(cls):
        return cls.metadata.tables[cls.__tablename__].columns.keys()

    @property
    def fields(self):
        return dict(object_mapper(self).columns).keys()

    @classmethod
    def get_sortable(cls):
        excludes = getattr(cls, '_sortable_excludes', [])
        return set(cls.get_fields()) - set(excludes)

    @classmethod
    def get_searchable(cls):
        excludes = getattr(cls, '_searchable_excludes', [])
        return set(cls.get_fields()) - set(excludes)

    def to_dict(self):
        json_fields = self._json_fields
        obj = {}
        for field in self.fields:
            attr = getattr(self, field)

            if field in json_fields:
                obj[field] = jsonutils.loads(attr)
            else:
                obj[field] = attr

        return obj


class Event(BASE, BaseModel):

    __tablename__ = 'events'
    __table_args__ = (
        Index('event_message_id', 'message_id'),
        Index('project_name_x_user_name_idx',
              'project_name', 'user_name'),
        Index('project_id_x_user_id_idx',
              'project_id', 'user_id'),
        Index('request_id', 'request_id'),
    )

    _sortable_excludes = ['raw_message', 'raw_message_id',
                          'payload', 'roles']
    _searchable_excludes = ['raw_message', 'raw_message_id',
                            'payload', 'roles']
    _json_fields = ['roles', 'payload']

    id = Column(Integer, primary_key=True)
    object_id = Column(String(100))
    message_id = Column(String(100))
    token = Column(String(100), nullable=False)
    raw_message_id = Column(Integer, ForeignKey('raw_messages.id'))
    raw_message = relationship('RawMessage', backref="event", uselist=False)
    #FIXME: duplicated column
    token = Column(String(100))
    is_admin = Column(Boolean, default=False)
    request_id = Column(String(100))
    # list
    roles = Column(String(100))
    project_id = Column(String(100))
    project_name = Column(String(100))
    user_name = Column(String(100))
    user_id = Column(String(100))
    event_type = Column(String(100))
    payload = Column(Text())
    level = Column(String(20))
    remote_address = Column(String(20))
    publisher_id = Column(String(100))
    timestamp = Column(DateTime())
    hostname = Column(String(50))
    binary = Column(String(20))
    # e.g. nova, cinder, glance
    service = Column(String(20))


class RawMessage(BASE, BaseModel):

    __tablename__ = 'raw_messages'
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    json = Column(Text, nullable=False)
