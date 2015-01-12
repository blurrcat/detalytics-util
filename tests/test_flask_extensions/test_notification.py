#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mock import Mock
from util.flask_extensions.notification import Notification


def test_send_sms(app):
    notification = Notification(app)
    notification.twilio = Mock()
    user = 'blurrcat'
    r = notification.send_sms(
        '+8618615729525', 'sms', user=user)
    assert user in r
    _send_sms = notification.twilio.messages.create
    assert _send_sms.called
    assert user in str(_send_sms.call_args)


def test_send_email(app):
    notification = Notification(app)
    mail = app.extensions['mail']
    user = 'blurrcat'
    with mail.record_messages() as outbox:
        notification.send_mail(
            'battery low', 'blurrcat@gmail.com', 'email.txt', user=user)
        assert len(outbox) == 1
        sent = outbox[0]
        assert 'battery' in sent.subject
        assert user in sent.body
        assert sent.html is None
    with mail.record_messages() as outbox:
        notification.send_mail(
            'battery low', 'blurrcat@gmail.com', 'email.txt', 'email.html',
            user=user)
        assert user in outbox[0].html

