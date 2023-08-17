from configparser import ConfigParser
import redis


class RedisConnector:
    def __init__(self, config: ConfigParser):
        self.RD_HOST = config.get("Redis","HOST")
        self.RD_PORT = int(config.get("Redis","PORT"))
        self.RD_USER = config.get("Redis","USER")
        self.RD_PASS = config.get("Redis","PASS")
        self.RD_INDEX = int(config.get("Redis","INDEX"))

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

    def get_cache(self, key):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.get(key)

    def set_cache(self, key, val):
        channel = redis.Redis(connection_pool=self.redis_pool)
        return channel.set(key, val)
