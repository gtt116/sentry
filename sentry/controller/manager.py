#
# Created on 2012-11-16
#
# @author: hzyangtk
#

import logging as std_logging
import eventlet
from oslo.config import cfg

from sentry.openstack.common import log
from sentry.openstack.common import rpc
from sentry.openstack.common import importutils
from sentry.openstack.common import jsonutils

"""
    Sentry listenning on rabbitmq and receive notification
    from nova-compute, nova-service-monitor, nova-cloudwatch,
    nova-network, nova-billing, nova-api, nova-scheduler.
    When received a notification, it will filter the notification
    and send a alarm message to alarm system when the notification
    is alarm level.
"""


manager_configs = [
    cfg.StrOpt('queue_suffix',
               default='sentry',
               help='Name of queue suffix'),
    cfg.StrOpt('nova_sentry_mq_topic',
               default='notifications',
               help='Name of nova notifications topic'),
    cfg.StrOpt('glance_sentry_mq_topic',
               default='glance_notifications',
               help='Name of glance notifications topic'),
    cfg.StrOpt('neutron_sentry_mq_topic',
               default='neutron_notifications',
               help='Name of neutron notifications topic'),
    cfg.StrOpt('cinder_sentry_mq_topic',
               default='cinder_notifications',
               help='Name of neutron notifications topic'),
    cfg.ListOpt('nova_mq_level_list',
                default=['error', 'info', ],
                help='notifications levels for message queue of nova'),
    cfg.ListOpt('glance_mq_level_list',
                default=['error', 'info', 'warn', ],
                help='notifications levels for message queue of glance'),
    cfg.ListOpt('neutron_mq_level_list',
                default=['error', 'info', 'warn', ],
                help='notifications levels for message queue of neutron'),
    cfg.ListOpt('cinder_mq_level_list',
                default=['error', 'info', 'warn', ],
                help='notifications levels for message queue of neutron'),
]

handlers = [
    cfg.ListOpt('nova_event_handlers',
                default=['alarm', 'nova'],
                help="Nova event handlers"),
    cfg.ListOpt('cinder_event_handlers',
                default=['alarm', 'cinder'],
                help="cinder event handlers"),
    cfg.ListOpt('neutron_event_handlers',
                default=['alarm', 'neutron'],
                help="neutron event handlers"),
    cfg.ListOpt('glance_event_handlers',
                default=['alarm', 'glance'],
                help="glance event handlers"),
]

CONF = cfg.CONF
CONF.register_opts(manager_configs)
CONF.register_opts(handlers)
LOG = log.getLogger(__name__)


class Pipeline(object):
    def __init__(self, handlers):
        self.handlers = handlers

    def process(self, message):
        if isinstance(message, basestring):
            message = jsonutils.loads(message)
        if not isinstance(message, dict):
            LOG.warn("Message is not a dict object: %s" % message)

        for handler in self.handlers:
            try:
                handler.handle_message(message)
            except Exception:
                LOG.exception("%s process message error, skip it." % handler)


class Manager(object):

    def __init__(self):
        self.conn = rpc.create_connection(new=True)
        # faild early
        self.nova_handlers = self.registry_handlers(
            CONF.nova_event_handlers)
        self.nova_pipeline = Pipeline(self.nova_handlers)

        self.cinder_handlers = self.registry_handlers(
            CONF.cinder_event_handlers)
        self.cinder_pipeline = Pipeline(self.cinder_handlers)

        self.neutron_handlers = self.registry_handlers(
            CONF.neutron_event_handlers)
        self.neutron_pipeline = Pipeline(self.neutron_handlers)

        self.glance_handlers = self.registry_handlers(
            CONF.glance_event_handlers)
        self.glance_pipeline = Pipeline(self.glance_handlers)

    def registry_handlers(self, handler_names):
        prefix = "sentry.controller.handlers"
        class_name = "Handler"
        real_handlers = []
        for name in handler_names:
            path = "%s.%s.%s" % (prefix, name, class_name)
            try:
                obj = importutils.import_object(path)
                real_handlers.append(obj)
            except ImportError:
                LOG.exception("import %(path)s error, ignore this handler" %
                              {'path': path})
        return real_handlers

    def serve(self):
        """
        The default notification topic is:
            "topic = '%s.%s' % (topic, priority)"

        Example:
            "notifications.info"
        """
        CONF.log_opt_values(LOG, std_logging.DEBUG)
        LOG.info('Start sentry service.')

        # Nova
        self._declare_queue_consumer(
            CONF.nova_mq_level_list,
            CONF.nova_sentry_mq_topic,
            self.nova_pipeline.process,
        )

        # neutron
        self._declare_queue_consumer(
            CONF.neutron_mq_level_list,
            CONF.neutron_sentry_mq_topic,
            self.neutron_pipeline.process,
        )

        # glance
        self._declare_queue_consumer(
            CONF.glance_mq_level_list,
            CONF.glance_sentry_mq_topic,
            self.glance_pipeline.process,
        )

        # cinder
        self._declare_queue_consumer(
            CONF.cinder_mq_level_list,
            CONF.cinder_sentry_mq_topic,
            self.cinder_pipeline.process,
        )

        self.conn.consume_in_thread()
        LOG.info('Start consuming notifications.')

    def _declare_queue_consumer(self, levels, topic, handler):
        def queue_name(topic, level):
            return '%s.%s' % (topic, level)

        for level in levels:
            queue = queue_name(topic, level)
            self.conn.declare_topic_consumer(
                topic=topic,
                callback=handler,
                queue_name=queue,
            )
            LOG.debug("Declare queue name: %(queue)s, topic: %(topic)s" %
                      {"queue": queue, "topic": topic})

    def create(self):
        return eventlet.spawn(self.serve())

    def cleanup(self):
        LOG.info('Cleanup sentry')
        rpc.cleanup()
