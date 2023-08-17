from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector


class Comic:
    def __init__(self, **kwargs):
        DB: MysqlConnector = kwargs.get('DB_POOL')
        RD: RedisConnector = kwargs.get('RD_POOL')
        BOT:Bot = kwargs.get('BOT_POOL')
        print(DB.get_conn(),RD,BOT)

