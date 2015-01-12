#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from util.celery_utils import create_celery


def test_create_celery():
    app = Flask('test_create_celery')
    celery_config = {
        'CELERY_BROKER_URL': 'redis://localhost/0',
    }
    app.config.update(celery_config)
    celery = create_celery(app)
    for k in celery_config:
        assert celery.conf[k] == celery_config[k]
    assert app.extensions['celery'] == celery
