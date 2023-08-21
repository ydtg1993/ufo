from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MysqlConnector:
    def __init__(self, config):
        self.DB_HOST = config.get("Database", "HOST")
        self.DB_PORT = int(config.get("Database", "PORT"))
        self.DB_USER = config.get("Database", "USER")
        self.DB_PASS = config.get("Database", "PASS")
        self.DB_NAME = config.get("Database", "DB")
        try:
            self.engine = create_engine(
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}",
                pool_size=20, max_overflow=0)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except BaseException as e:
            print(f'{e}')
        else:
            print('mysql链接成功')
