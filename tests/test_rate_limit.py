#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import uuid
from mock import Mock
import pytest
from util.rate_limit import RateLimiter


@pytest.fixture
def identity():
    return uuid.uuid4().hex

@pytest.fixture(scope='session')
def limiter():
    logging.basicConfig(level=logging.DEBUG)
    return RateLimiter()


@pytest.fixture
def patch_time(monkeypatch):
    mock = Mock(return_value=0)
    monkeypatch.setattr('time.time', mock)
    return mock


def test_single_limit(identity, patch_time, limiter):
    limit = 2
    duration = 1

    def over_limit():
        return limiter.over_limit(identity, ((duration, limit),))
    # within limit
    for i in xrange(limit):
        assert not over_limit()
    # over limit
    assert over_limit()
    # within limit again in next second
    patch_time.return_value = 1
    assert not over_limit()


def test_multi_limit(identity, patch_time, limiter):
    def over_limit():
        return limiter.over_limit(identity, (
            (1, 2),  # 2/sec
            (2, 3),  # 3/2sec
        ))
    # if we request at 3 req/sec, then the limits should be as follows::
    #
    #     over limit:   f   f   t   f   t   t
    #     time      : 0-----------1-----------2
    #
    for expectation in [False, False, True]:
        assert over_limit() == expectation
    patch_time.return_value = 1
    for expectation in [False, True, True]:
        assert over_limit() == expectation

