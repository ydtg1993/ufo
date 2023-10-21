from configparser import ConfigParser
from assiatant.bot import Bot
from assiatant.rd import RedisConnector


class Globe:
    process_cache_conf = []

    def __init__(self, config: ConfigParser, connects: dict, redis: RedisConnector, bot: Bot):
        self.config = config
        self.mysql = connects
        self.redis = redis
        self.bot = bot
