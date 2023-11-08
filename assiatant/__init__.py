import configparser
import os
from assiatant.globe import Globe
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector
import logging.handlers

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    'detail': {'key': GB.config.get("App", "PROJECT") + ":detail:task", 'name': '基础信息队列', 'type': 'queue'},
    'hook_video': {'key': GB.config.get("App", "PROJECT") + ":hook:video", 'name': '视频锚', 'type': 'cache'},
    'hook_cover': {'key': GB.config.get("App", "PROJECT") + ":hook:big_cover", 'name': '大图锚', 'type': 'cache'},
    'av.unique': {'key': GB.config.get("App", "PROJECT") + ":unique:video:link", 'name': '片子去重hash', 'type': 'hash'},
}
