import os
import redis
from dotenv import load_dotenv

class RedisConnector:
    def __init__(self):
        load_dotenv()
        self.RD_HOST = os.getenv("RD_HOST", "localhost")
        self.RD_PORT = os.getenv("RD_PORT", 6379)
        self.RD_USER = os.getenv("RD_USER", "root")
        self.RD_PASS = os.getenv("RD_PASS", "")
        self.RD_INDEX = os.getenv("RD_INDEX", 0)

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
