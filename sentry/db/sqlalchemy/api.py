import sys

from sqlalchemy.sql.expression import desc, asc

from sentry.db.sqlalchemy import session
from sentry.db.sqlalchemy import models
from sentry.openstack.common import jsonutils


def get_backend():
    return sys.modules[__name__]


def event_create(event):
    se = session.get_session()

    # dump to json
    raw_json = jsonutils.dumps(event.raw_json)
    raw_message = models.RawMessage(json=raw_json)
    se.add(raw_message)

    event = models.Event(
        message_id=event.message_id,
        token=event.token,
        object_id=event.object_id,
        raw_message=raw_message,
        is_admin=event.is_admin,
        request_id=event.request_id,
        roles=jsonutils.dumps(event.roles),  # json
        project_id=event.project_id,
        project_name=event.project_name,
        user_name=event.user_name,
        user_id=event.user_id,
        event_type=event.event_type,
        payload=jsonutils.dumps(event.payload),  # json
        level=event.level,
        publisher_id=event.publisher_id,
        remote_address=event.remote_address,
        timestamp=event.timestamp,
        service=event.service,
        binary=event.binary,
        hostname=event.hostname,
    )
    se.add(event)
    se.commit()


def _validate_search_dict(model, search_dict):
    """
    Inspect search dict contains invalid key of model searchable.
    """
    can_search = model.get_searchable()
    for key in search_dict.keys():
        if not key in can_search:
            msg = ("search by %(key)s invalid, only support: %(can)s" %
                    {'key': key, 'can': can_search})
            raise ValueError(msg)


def _validate_sort_keys(model, sort_keys):
    """
    Inspect sort_keys is searchable in model, if not raise ValueError.
    Return a new list contains sqlalchemy sort criterion.
    """
    sorts_criterion = []
    can_sort = model.get_sortable()

    if not sort_keys:
        return []

    for key in sort_keys:
        neg = False
        if key[0] == '-':
            key = key[1:]

        if not (key in can_sort):
            msg = ("sort by %(key)s invalid, only support: %(can)s" %
                   {'key': key, 'can': can_sort})
            raise ValueError(msg)

        if neg:
            criterion = desc(getattr(model, key))
        else:
            criterion = asc(getattr(model, key))

        sorts_criterion.append(criterion)
    return sorts_criterion


def event_get_all(search_dict={}, sorts=[]):
    se = session.get_session()

    # failed fast
    if search_dict:
        _validate_search_dict(models.Event, search_dict)

    sorts_criterion = _validate_sort_keys(models.Event, sorts)

    query = se.query(models.Event)

    if search_dict:
        query = query.filter_by(**search_dict)

    for sort in sorts_criterion:
        query = query.order_by(sort)

    return query


def event_schema():
    fields = models.Event.get_fields()
    sortables = models.Event.get_sortable()
    searchable = models.Event.get_searchable()
    return fields, sortables, searchable
