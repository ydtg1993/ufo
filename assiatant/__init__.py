import configparser
import time
from assiatant.globe import GB
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector

config = configparser.ConfigParser()
config.read('config.ini')
GB["config"] = config
GB["mysql"] = MysqlConnector(config)
GB["redis"] = RedisConnector(config)
GB["bot"] = Bot(config)
GB["bot"].start_pool(int(config.get("Bot", "MAX_THREADS")))