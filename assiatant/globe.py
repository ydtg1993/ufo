from configparser import ConfigParser
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector


class Globe:
    def __init__(self, config: ConfigParser, mysql: MysqlConnector, redis: RedisConnector, bot: Bot):
        self.config = config
        self.mysql = mysql
        self.redis = redis
        self.bot = bot