from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
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
                f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?auth_plugin=mysql_native_password&autocommit=true",
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
            self.engine.dispose()
            self.connect()
        except BaseException as e:
            print(f'{e}')
        else:
            print('mysql重新链接成功')
