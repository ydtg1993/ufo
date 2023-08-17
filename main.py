import time
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector
from controller.comic import Comic

def main():
    tools = dict(
        DB_POOL=MysqlConnector(),
        RD_POOL=RedisConnector(),
        BOT_POOL=Bot(1),)
    time.sleep(5)
    Comic(**tools)


if __name__ == '__main__':
    main()
    input("按任意键退出...")