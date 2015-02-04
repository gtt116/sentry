#!/usr/bin/env python

"""
NVS Alarm module
"""

import os
import sys


# If ../sentry/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir, os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'sentry', '__init__.py')):
    sys.path.insert(0, possible_topdir)

import eventlet
import logging as std_logging
from oslo.config import cfg

from sentry.common import config
from sentry.controller import manager
from sentry.openstack.common import log

LOG = log.getLogger(__name__)
CONF = cfg.CONF


def main():
    config.parse_args(sys.argv[1:])
    log.setup('sentry')
    eventlet.monkey_patch(os=False)

    mgr = manager.Manager()
    # After manager instantiated, some handler will be imported
    CONF.log_opt_values(LOG, std_logging.DEBUG)
    mgr.run_server()
    mgr.wait()
