import redis


class RedisWrapper:
    def connect(self):
        connection_pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
        return redis.StrictRedis(connection_pool=connection_pool)
