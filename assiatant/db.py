from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser


class MysqlConnector:
    session = None

    def __init__(self, config: ConfigParser):
        self.DB_HOST = config.get("Database", "HOST")
        self.DB_PORT = int(config.get("Database", "PORT"))
        self.DB_USER = config.get("Database", "USER")
        self.DB_PASS = config.get("Database", "PASS")
        self.DB_NAME = config.get("Database", "DB")
        try:
            self.engine = create_engine(
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
                pool_size=20, max_overflow=10)
            self.connect()
        except BaseException as e:
            print(f'{e}')
        else:
            print('mysql链接成功')

    def connect(self):
        try:
            self.engine.connect()
            session = sessionmaker(bind=self.engine)
            self.session = session()
            print('MySQL connection successful')
        except OperationalError as e:
            print(f'Error connecting to MySQL: {e}')

    def reconnect(self):
        try:
            self.session.close()
            self.engine.dispose()
            self.connect()
        except BaseException as e:
            print(f'{e}')
        else:
            print('mysql重新链接成功')

    def try_reconnect(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            if "MySQL server has gone away" in str(e):
                self.reconnect()
                return self.try_reconnect(func, *args, **kwargs)
            else:
                raise
