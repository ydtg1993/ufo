from configparser import ConfigParser
from dbutils.pooled_db import PooledDB
import pymysql


class MysqlConnector:
    def __init__(self, config: ConfigParser):
        self.DB_HOST = config.get("Database", "HOST")
        self.DB_PORT = int(config.get("Database", "PORT"))
        self.DB_USER = config.get("Database", "USER")
        self.DB_PASS = config.get("Database", "PASS")
        self.DB_NAME = config.get("Database", "DB")

        try:
            self.mysql_pool = PooledDB(creator=pymysql,  # 数据库类型
                                       maxcached=20,  # 最大空闲数
                                       blocking=True,  # 默认False，即达到最大连接数时，再取新连接将会报错，True，达到最大连接数时，新连接阻塞，等待连接数减少再连接
                                       ping=4,
                                       host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER,
                                       password=self.DB_PASS,
                                       db=self.DB_NAME,
                                       charset='utf8')
            self.mysql_pool.connection()
        except BaseException as e:
            print(f'数据库链接错误{e}')
        else:
            print('数据库链接成功')

    def get_conn(self):
        conn = self.mysql_pool.connection()
        cur = conn.cursor()
        return conn, cur

    def close_conn(self, conn, cur):
        cur.close()
        conn.close()

    def select_infor(self, insert):
        conn, cur = self.get_conn()
        try:
            cur.execute(insert)
            return cur.fetchall()
        except BaseException as e:
            print('数据库查询错误')
        finally:
            self.close_conn(conn, cur)

    def update_infor(self, insert):
        conn, cur = self.get_conn()
        try:
            cur.execute(insert)
            conn.commit()
            return True
        except BaseException as e:
            print(f'数据库更新错误{e}')
        finally:
            self.close_conn(conn, cur)

    def insert_data(self, table: str, data_dict: dict):
        conn, cur = self.get_conn()
        try:
            placeholders = ', '.join(['%s'] * len(data_dict))
            columns = ', '.join(data_dict.keys())
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

            # 执行单条记录插入
            cur.execute(sql, tuple(data_dict.values()))

            conn.commit()  # 提交事务
            return True
        except BaseException as e:
            conn.rollback()  # 回滚事务
            print(f'数据库插入错误: {e}')
            return False
        finally:
            self.close_conn(conn, cur)
