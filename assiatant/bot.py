import os
import threading
import undetected_chromedriver as uc
from dotenv import load_dotenv

class Bot(object):
    pool = []
    pool_lock = threading.Lock()
    def __init__(self, n=1):
        for i in range(n):
            thread = threading.Thread(target=self.beginning, args=())
            thread.start()

    def beginning(self):
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options, user_multi_procs=True)
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
