import time
from undetected_chromedriver import Chrome
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector


class Comic:
    def __init__(self, **kwargs):
        DB: MysqlConnector = kwargs.get('DB_POOL')
        RD: RedisConnector = kwargs.get('RD_POOL')
        BOT:Bot = kwargs.get('BOT_POOL')
        WebDriver:Chrome = BOT.get_driver()
        WebDriver.get("https://baidu.com")


