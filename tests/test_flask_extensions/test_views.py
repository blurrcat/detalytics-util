#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import Flask
from util.flask_extensions.health import Health


def test_health():
    app = Flask('test_health')
    Health(app)
    with app.test_client() as c:
        r = c.get('/_health')
        assert r.status_code == 200
        r = json.loads(r.data)
        for key in ('git', 'packages', 'app', 'status'):
            assert key in r
