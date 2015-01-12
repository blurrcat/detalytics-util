#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import request, Response
from util.flask_extensions.request_monitor import RequestMonitor


def make_log(logger):
    log = logger.info.call_args[0][0] % logger.info.call_args[0][1:]
    print log
    return log


def test_request_log(app, patched_logger):
    @app.route('/books/<int:bid>', methods=['GET', 'POST'])
    def index(bid):
        if request.method == 'GET':
            return 'book %d' % bid
        else:
            return Response(status=201)

    monitor = RequestMonitor(app)

    book_id = '10'
    content = 'bible'
    path = '/books/%s' % book_id
    headers = {
        'content-type': 'application/json'
    }

    with app.test_client() as c:
        # test get and header
        r = c.get(path)
        assert r.status_code == 200
        log = make_log(monitor.logger)
        assert path in log
        monitor.logger.info.reset_mock()

        r = c.post(path, data=json.dumps({'content': content}), headers=headers)
        assert r.status_code == 201
        log = make_log(monitor.logger).lower()
        for part in (content, headers['content-type']):
            assert part in log
