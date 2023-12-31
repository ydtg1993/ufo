import configparser
import time
import schedule
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.globe import GB
from assiatant.rd import RedisConnector
from controller.comic import Comic


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    GB["config"] = config
    GB["mysql"] = MysqlConnector(config)
    GB["redis"] = RedisConnector(config)
    GB["bot"] = Bot(config)
    Comic()

    schedule.every(6).hours.do(Comic)
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    main()
