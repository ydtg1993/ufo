import time
from undetected_chromedriver import Chrome
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.proxy import Proxy
from assiatant.rd import RedisConnector
from configparser import ConfigParser


class Comic:
    def __init__(self, **kwargs):
        CONF: ConfigParser = kwargs.get('CONF')
        DB: MysqlConnector = kwargs.get('DB_POOL')
        RD: RedisConnector = kwargs.get('RD_POOL')
        BOT: Bot = kwargs.get('BOT_POOL')

        Proxy(RD, CONF).get_proxy()
