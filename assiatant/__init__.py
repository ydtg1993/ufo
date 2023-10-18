import configparser
from assiatant.globe import Globe
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector
import logging
import logging.handlers

fh = logging.handlers.TimedRotatingFileHandler('app.log', when='midnight', backupCount=7, encoding='utf8')
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                    level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    handlers=[fh])

config = configparser.ConfigParser()
config.read('config.ini')
GB = Globe(config, MysqlConnector(config), RedisConnector(config), Bot(config))
GB.menu_tick = {}
GB.menu_tick_limit = 5
