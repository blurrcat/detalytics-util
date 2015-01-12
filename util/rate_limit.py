#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import redis
import time


class RateLimiter(object):

    def __init__(
            self, redis_host='localhost', redis_port=6379, redis_db=0,
            redis_password=None, key_prefix='rl', logger=None):
        self._r = redis.Redis(
            host=redis_host, port=redis_port, db=redis_db,
            password=redis_password)
        self._prefix = key_prefix
        self._logger = logger or logging.getLogger('rate_limiter')

    def over_limit(self, identity, duration_limits):
        """
        Check if the rate of the given identify is over limit

        :param identity: identity to check rate limit
        :param list duration_limits:
            a list of limits for different durations. For example, to ensure
            requests number is < 1000 in an hour and < 60 in a minute, set
            `duration_limits` to `((3600, 1000), (60, 60))`.
        :return: True if limit has been reached.
        """
        pipeline = self._r.pipeline(transaction=True)
        now = time.time()
        for duration, limit in duration_limits:
            bucket = '%s:%s:%i:%i' % (
                self._prefix, identity, duration, now // duration)
            pipeline.incr(bucket)
            pipeline.expire(bucket, duration)
        results = pipeline.execute()
        over_limit = False
        for i, (duration, limit) in enumerate(duration_limits):
            self._logger.debug(
                'hits %i@%.1f[limit %i per %i sec]: %s',
                results[i * 2], now, limit, duration,
                '%s:%s:%i:%i' % (
                    self._prefix, identity, limit, now // duration)
            )
            if results[i * 2] > limit:
                over_limit = True
                # calibrate hits: only count successful ones
                pipeline.decr('%s:%s:%i:%i' % (
                    self._prefix, identity, limit, now // duration))
                # TODO: reduce this extra round-trip with LUA scripting
        pipeline.execute()
        return over_limit
