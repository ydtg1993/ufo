from configparser import ConfigParser
import redis


class RedisConnector:
    def __init__(self, config: ConfigParser):
        self.RD_HOST = config.get("Redis", "HOST")
        self.RD_PORT = int(config.get("Redis", "PORT"))
        self.RD_USER = config.get("Redis", "USER")
        self.RD_PASS = config.get("Redis", "PASS")
        self.RD_INDEX = int(config.get("Redis", "INDEX"))

        try:
            self.redis_pool = redis.ConnectionPool(
                host=self.RD_HOST,
                port=self.RD_PORT,
                db=self.RD_INDEX,
                password=self.RD_PASS,
                decode_responses=True
            )
            connection = redis.Redis(connection_pool=self.redis_pool)
            connection.ping()
        except BaseException as e:
            print(f'{e}')
        else:
            print('redis链接成功')

    def get_cache(self, key: str):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.get(key)

    def set_cache(self, key: str, val: str, expire_time: int = 0):
        if expire_time > 0:
            channel = redis.Redis(connection_pool=self.redis_pool)
            return channel.setex(key, expire_time, val)
        else:
            channel = redis.Redis(connection_pool=self.redis_pool)
            return channel.set(key, val)

    def get_hash(self, hash_name: str, field: str):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.hget(hash_name, field)

    def set_hash(self, hash_name: str, field: str, value: str):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.hset(hash_name, field, value)

    def get_hash_keys(self, hash_name: str):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.hkeys(hash_name)

    def enqueue(self, queue_name: str, item: str):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.lpush(queue_name, item)

    def dequeue(self, queue_name: str):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.rpop(queue_name)

    def get_queue(self, queue_name: str, start: int, end: int):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.lrange(queue_name, start, end)

    def delete(self, key: str):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.delete(key)

    def delete_keys_pattern(self, pattern: str):
        channel = redis.Redis(connection_pool=self.redis_pool)
        keys_to_delete = channel.keys(pattern)
        deleted_keys_count = 0
        for key in keys_to_delete:
            result = channel.delete(key)
            deleted_keys_count += result
        return deleted_keys_count
