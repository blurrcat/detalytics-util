#!/usr/bin/env python
# -*- coding: utf-8 -*-


class FlaskExtension(object):

    def __init__(self, app=None, **kwargs):
        self.app = app
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        pass
