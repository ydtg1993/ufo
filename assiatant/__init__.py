import configparser
import os
from assiatant.globe import Globe
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector
import logging.handlers

# timezone setting
os.environ["TZ"] = "Asia/Shanghai"

# log setting
fh = logging.handlers.TimedRotatingFileHandler('./log/app.log', when='midnight', backupCount=7, encoding='utf8',
                                               delay=True)
fh.setLevel(logging.WARNING)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s",
                    level=logging.DEBUG,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    handlers=[fh])

# config setting
config = configparser.ConfigParser()
config.read('config.ini')

# globe setting
GB = Globe(config, MysqlConnector(config), RedisConnector(config), Bot(config))

# step cache key setting
GB.process_cache_conf = {
    'comics': {'key': GB.config.get("App", "PROJECT") + ":comics", 'name': '漫画信息录入队列', 'type': 'queue'},
    'comics.unique': {'key': GB.config.get("App", "PROJECT") + ":comics:link", 'name': '漫画去重hash', 'type': 'hash'},
    'chapters': {'key': GB.config.get("App", "PROJECT") + ":chapters", 'name': '章节信息录队列', 'type': 'queue'},
    'chapters.unique': {'key': GB.config.get("App", "PROJECT") + ":chapters:link", 'name': '章节去重hash', 'type': 'hash'},
    'images': {'key': GB.config.get("App", "PROJECT") + ":chapters:images", 'name': '图片', 'type': 'cache'},
}
