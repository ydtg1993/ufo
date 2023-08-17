from configparser import ConfigParser
import redis


class RedisConnector:
    def __init__(self, config: ConfigParser):
        self.RD_HOST = config.get("Redis","HOST")
        self.RD_PORT = config.get("Redis","PORT")
        self.RD_USER = config.get("Redis","USER")
        self.RD_PASS = config.get("Redis","PASS")
        self.RD_INDEX = config.get("Redis","INDEX")

        try:
            self.redis_pool = redis.ConnectionPool(
                host=self.RD_HOST,
                port=self.RD_PORT,
                db=self.RD_INDEX,
                username=self.RD_USER,
                password=self.RD_PASS,
                decode_responses=True
            )
        except BaseException as e:
            print(f'读取配置文件错误：{e}')
        else:
            print('redis链接成功')

    def getCache(self, key):
        channel = redis.Redis(connection_pool=self.redis_pool)
        channel.get(key)

    def setCache(self, key, val):
        channel = redis.Redis(connection_pool=self.redis_pool)
        channel.set(key, val)
