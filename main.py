import time
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector
from controller.volume import Volume
import configparser
import schedule

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    tools = dict(
        CONF=config,
        DB_POOL=MysqlConnector(config),
        RD_POOL=RedisConnector(config),
        BOT_POOL=Bot(config), )
    time.sleep(3)
    run_volume_task(tools)

    schedule.every(6).hours.do(run_volume_task, tools)
    while True:
        schedule.run_pending()
        time.sleep(1200)

def run_volume_task(tools):
    Volume(**tools)

if __name__ == '__main__':
    main()
