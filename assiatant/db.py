import os
from dbutils.pooled_db import PooledDB
import pymysql
from dotenv import load_dotenv


class MysqlConnector:
    def __init__(self):
        load_dotenv()
        self.DB_HOST = os.getenv("DB_HOST","localhost")
        self.DB_PORT = os.getenv("DB_PORT",3306)
        self.DB_USER = os.getenv("DB_USER","root")
        self.DB_PASS = os.getenv("DB_PASS","123456")
        self.DB_NAME = os.getenv("DB_NAME","db")
        try:
            self.mysql_pool = PooledDB(creator=pymysql,  # 数据库类型
                                            maxcached=20,  # 最大空闲数
                                            blocking=True,  # 默认False，即达到最大连接数时，再取新连接将会报错，True，达到最大连接数时，新连接阻塞，等待连接数减少再连接
                                            ping=4,
                                            host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER,
                                            password=self.DB_PASS,
                                            db=self.DB_NAME,
                                            charset='utf8')
        except BaseException as e:
            print(f'数据库链接错误{e}')
        else:
            print('数据库链接成功')

    def get_conn(self):
        conn = self.mysql_pool.connection()
        cur = conn.cursor()
        return conn,cur

    def close_conn(self,conn,cur):
        cur.close()
        conn.close()

    def select_infor(self,insert):
        conn,cur = self.get_conn()
        try:
            cur.execute(insert)
            return cur.fetchall()
        except BaseException as e:
            print('数据库查询错误')
        finally:
            self.close_conn(conn,cur)

    def update_infor(self,insert):
        conn, cur = self.get_conn()
        try:
            cur.execute(insert)
            conn.commit()
            return True
        except BaseException as e:
            print(f'数据库更新错误{e}')
        finally:
            self.close_conn(conn, cur)