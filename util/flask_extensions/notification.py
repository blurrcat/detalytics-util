#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.mail import Message
from flask import current_app, render_template
from twilio.rest import TwilioRestClient


_DEFAULT_CONFIG = {
    'NOTIFICATION_TWILIO_VERSION': '2014-04-01',
}
REQUIRED_CONFIG = (
    'NOTIFICATION_MAIL_SENDER',
    'NOTIFICATION_TWILIO_SENDER',
    'NOTIFICATION_TWILIO_SID',
    'NOTIFICATION_TWILIO_TOKEN',
)


class Notification(object):
    """
    Send notification to users.

    Currently supports Email and SMS. To use this extension, flask-mail
    must be configured before sending any email::

        app = Flask('test')
        mail = Mail(app)
        notification = Notification(app)
        notification.send_mail(
            'test email', 'blurrcat@gmail.com', 'email.txt')

    """
    def __init__(self, app=None):
        self.app = app
        self.twilio = None
        self.mail = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        for key, val in _DEFAULT_CONFIG.iteritems():
            app.config.setdefault(key, val)
        for key in REQUIRED_CONFIG:
            if not key in app.config:
                raise RuntimeError(
                    'Missing required configuration key: %s', key)
        self.twilio = TwilioRestClient(
            account=app.config['NOTIFICATION_TWILIO_SID'],
            token=app.config['NOTIFICATION_TWILIO_TOKEN'],
            version=app.config['NOTIFICATION_TWILIO_VERSION'],
        )
        app.extensions.setdefault('notification', self)

    def send_mail(self, subject, recipient, txt_template, html_template=None,
                  **context):
        """
        Send an email. The body of the mail is rendered from the template.
        2 templates can be supplied, `txt_template` and `html_template`, which
        are set to corresponding mail attributes if presents.

        :param subject: subject of the mail.
        :param recipient: recipient of the mail.
        :param txt_template:
            path to template to render email body in plain text.
        :param html_template:
            path to template to render email body in html.
        :param context: additional template context.
        """
        msg = Message(
            subject, sender=current_app.config['NOTIFICATION_MAIL_SENDER'],
            recipients=[recipient])
        msg.body = render_template(txt_template, **context)
        if html_template:
            msg.html = render_template(html_template, **context)
        mail = current_app.extensions.get('mail')
        mail.send(msg)
        current_app.logger.debug(
            'sent email to %s: %s', recipient, msg.subject)
        return msg.body, msg.html

    def send_sms(self, recipient, template, media_urls=None, **context):
        """
        Send a SMS via twilio.
        The body of the message is rendered from the template.

        :param recipient: recipient of the SMS
        :param template: SMS template name
        :param media_urls: A list of URLs of images to include in the message
        :param context: additional template context
        """
        msg = render_template(template, **context)
        sent = self.twilio.messages.create(
            body=msg,
            to=recipient,
            from_=current_app.config['NOTIFICATION_TWILIO_SENDER'],
            media_urls=media_urls,
        )
        current_app.logger.debug('sent sms to %s: %s', recipient, sent)
        return msg
