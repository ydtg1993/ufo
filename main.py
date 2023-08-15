import time
from assiatant.bot import Bot
from dotenv import load_dotenv
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector


def main():
    global DB,RD
    DB = MysqlConnector()
    RD = RedisConnector()
    # Bot(2)

if __name__ == '__main__':
    main()
    input("按任意键退出...")