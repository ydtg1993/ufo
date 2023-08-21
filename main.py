import time
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector
from controller.volume import Volume
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

    schedule.every(2).hours.do(Volume(**tools))
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == '__main__':
    main()
