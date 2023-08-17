import threading
from configparser import ConfigParser
import undetected_chromedriver as uc


class Bot(object):
    pool = []
    pool_lock = threading.Lock()

    def __init__(self, config: ConfigParser):
        num = int(config.get("Bot", "thread"))
        for i in range(num):
            self.beginning()

    def beginning(self):
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options, user_multi_procs=True)
        with self.pool_lock:
            self.pool.append(driver)

    def get_driver(self):
        with self.pool_lock:
            if self.pool:
                return self.pool.pop()
            else:
                return None

    def release_driver(self, driver):
        with self.pool_lock:
            self.pool.append(driver)
