from configparser import ConfigParser
from assiatant.db import MysqlConnector
from assiatant.bot import Bot
from assiatant.rd import RedisConnector


class Globe:
    process_cache_conf = []

    def __init__(self, config: ConfigParser, mysql: MysqlConnector, redis: RedisConnector, bot: Bot):
        self.config = config
        self.mysql = mysql
        self.redis = redis
        self.bot = bot
