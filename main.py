import threading
import time
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector
from controller.comic import Comic
import configparser

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    tools = dict(
        CONF=config,
        DB_POOL=MysqlConnector(config),
        RD_POOL=RedisConnector(config),
        BOT_POOL=Bot(config), )
    time.sleep(3)

    for t in range(3):
        thread = threading.Thread(target=Comic, kwargs=tools)
        thread.start()


if __name__ == '__main__':
    main()
    input("按任意键退出...")
