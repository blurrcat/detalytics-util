#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery import Celery
from raven.contrib.celery import CeleryFilter, register_signal
from raven.handlers.logging import SentryHandler


def create_celery(app, name=None):
    celery = Celery(name or app.name, broker=app.config['CELERY_BROKER_URL'])
    for k in app.config:
        if k.startswith('CELERY'):
            celery.conf[k] = app.config[k]

    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    logger = celery.log.get_default_logger()
    for handler in app.logger.handlers:
        if isinstance(handler, SentryHandler):
            handler.addFilter(CeleryFilter())
        logger.addHandler(handler)

    if 'sentry' in app.extensions:
        raven_client = app.extensions['sentry'].client
        register_signal(raven_client)
    logger.info("celery started")

    app.extensions.setdefault('celery', celery)
    return celery
