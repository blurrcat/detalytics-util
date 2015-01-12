#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
from flask import request
from util.flask_extensions.base import FlaskExtension


class RequestMonitor(FlaskExtension):

    def __init__(self, app=None, **kwargs):
        self.logger = None
        super(RequestMonitor, self).__init__(app, **kwargs)

    def log_before_request(self):
        """
        Example: 10.1.1.9 - POST - /index.html data
        :return:
        """
        self.logger.info(
            '[%s - %s - %s]Headers: %s - Data: %s',
            request.remote_addr or '?', request.method, request.base_url,
            json.dumps(dict(request.headers)), request.data)

    def init_app(self, app, **kwargs):
        self.logger = logging.getLogger('%s.monitor' % app.logger.name)
        app.before_request(self.log_before_request)
