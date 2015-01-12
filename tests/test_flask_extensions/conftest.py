#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mail import Mail
from mock import MagicMock
import pytest


@pytest.fixture
def template_folder(tmpdir):
    path = tmpdir.mkdir('templates')
    path.join('email.txt').write('''
Hi {{ user }},
    Your battery is running low!
    ''')
    path.join('email.html').write('''
    <html>
        <body>
        <h1>Hi {{ user }},</h1>
        <p>Your battery is running low!</p>
        </body>
    </html>''')
    path.join('sms').write('Hi {{ user }}, your battery is running low')
    return path.strpath


@pytest.fixture
def patched_logger(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr('logging.getLogger', lambda name: mock)
    return mock


@pytest.fixture
def app(request, template_folder):
    a = Flask('test', template_folder=template_folder)
    a.config.update({
        'DEBUG': True,
        'TESTING': True,
        'NOTIFICATION_MAIL_SENDER': 'test@detalytics.com',
        'NOTIFICATION_TWILIO_SENDER': '+123',
        'NOTIFICATION_TWILIO_SID': '123',
        'NOTIFICATION_TWILIO_TOKEN': '123',
    })
    Mail(a)

    ctx = a.app_context()
    ctx.push()

    def clean():
        ctx.pop()

    request.addfinalizer(clean)
    return a
