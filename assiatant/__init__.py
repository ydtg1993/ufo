import configparser
from assiatant.globe import Globe
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector

config = configparser.ConfigParser()
config.read('config.ini')
GB = Globe(config, MysqlConnector(config), RedisConnector(config), Bot(config))