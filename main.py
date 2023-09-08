import configparser
import time
import schedule
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.globe import GB
from assiatant.rd import RedisConnector
from controller.news import News


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    GB["config"] = config
    GB["mysql"] = MysqlConnector(config)
    GB["redis"] = RedisConnector(config)
    GB["bot"] = Bot(config)
    GB["bot"].start_pool(int(config.get("Bot", "MAX_THREADS")))
    News()

    schedule.every(1).hours.do(News)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
