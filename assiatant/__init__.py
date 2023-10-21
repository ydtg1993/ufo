import configparser
from assiatant.globe import Globe
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector
import logging.handlers

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
GB = Globe(config, {
    'comic': MysqlConnector(config),
    'img': MysqlConnector(config),
    'reset_comic_update_queue': MysqlConnector(config),
    'reset_chapter_img_queue': MysqlConnector(config),
},
           RedisConnector(config),
           Bot(config))
GB.menu_tick = {}

# step cache key setting
GB.process_cache_conf = {
    'comic': {'key': GB.config.get("App", "PROJECT") + ":comic:task", 'name': '漫画队列', 'type': 'info'},
    'img': {'key': GB.config.get("App", "PROJECT") + ":img:task", 'name': '章节抓图队列', 'type': 'info'},
    'chapter': {'key': GB.config.get("App", "PROJECT") + ":chapter:task", 'name': '章节更新队列', 'type': 'info'},
}
