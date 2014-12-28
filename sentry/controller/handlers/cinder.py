from sentry.openstack.common import log as logging

from sentry.controller import handlers
from sentry.db import models

LOG = logging.getLogger(__name__)


class Handler(handlers.PersistentHandler):
    def handle_message(self, msg):
        event = models.Event()
        event.service = 'cinder'

        try:
            event.token = msg['_context_auth_token']
            event.is_admin = msg['_context_is_admin']
            event.request_id = msg['_context_request_id']
            event.roles = msg['_context_roles']
            event.project_id = msg['_context_project_id']
            event.project_name = msg['_context_project_name']
            # FIXME:find a way to inject user_name into cinder
            # event.user_name = msg['_context_user_name']
            event.user_id = msg['_context_user_id']
            event.event_type = msg['event_type']
            event.message_id = msg['message_id']
            event.payload = msg['payload']
            event.level = msg['priority']
            event.publisher_id = msg['publisher_id']
            event.timestamp = msg['timestamp']
            event.remote_address = msg['_context_remote_address']
            event.catelog = msg['_context_service_catalog']
            event.object_id = msg['payload']['volume_id']
            event.binary, event.hostname = event.publisher_id.split('.')
        except Exception as ex:
            msg['exception'] = str(ex)
            msg['module'] = __name__
            self.save_unknown_event(msg)

        event.raw_id = self.save_notification(msg)
        self.save_event(event)
        return event
