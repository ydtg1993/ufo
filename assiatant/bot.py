import threading
import time
from configparser import ConfigParser
import undetected_chromedriver as uc


class Bot(object):
    pool = []
    pool_lock = threading.Lock()

    def __init__(self, config: ConfigParser):
        num = int(config.get("Bot", "thread"))

    def start(self):
        try:
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument("window-size=1920,1080")
            options.add_argument('--blink-settings=imagesEnabled=false')
            driver = uc.Chrome(options=options)
            driver.get("https://www.google.com")
            with self.pool_lock:
                self.pool.append(driver)
        except BaseException as e:
            print(f'webview开启失败{e}')

    def get_driver(self):
        with self.pool_lock:
            if self.pool:
                return self.pool.pop()
            else:
                return None
