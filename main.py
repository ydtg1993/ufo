import configparser
import time
import schedule
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.globe import GB
from assiatant.rd import RedisConnector
from controller.volume import Volume


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    GB["config"] = config
    GB["mysql"] = MysqlConnector(config)
    GB["redis"] = RedisConnector(config)
    GB["bot"] = Bot(config)
    Volume()

    schedule.every(6).hours.do(run_volume_task)
    while True:
        schedule.run_pending()
        time.sleep(900)

def run_volume_task():
    Volume()

if __name__ == '__main__':
    main()
