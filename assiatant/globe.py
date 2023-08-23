from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.rd import RedisConnector

GB = dict(config=dict, mysql=MysqlConnector, redis=RedisConnector, bot=Bot)
