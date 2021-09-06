import redis

from os import environ

class RedisHelper:
    def __init__(self):
        redis_pw = ""
        if environ['REDIS_PASSWORD']:
            redis_pw = environ['REDIS_PASSWORD']

        self.red = redis.StrictRedis(host="redis-primary", port=6379, db=0, password=redis_pw)

    def increment(self, key, amount):
        self.red.incr(key, amount = amount)