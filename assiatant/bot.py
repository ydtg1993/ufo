import cachetools
import random
import time
import requests
import undetected_chromedriver as uc
from configparser import ConfigParser


class Bot(object):
    _debug = None
    _proxy = None
    _mitm = None
    cache = cachetools.TTLCache(maxsize=100, ttl=800)

    def __init__(self, config: ConfigParser):
        self._debug = True if config.get("App", "DEBUG") == 'on' else False
        if config.get("Bot", "PROXY_URL"):
            self._proxy = config.get("Bot", "PROXY_URL")
        if config.get("Bot", "MITM_PROXY"):
            self._mitm = config.get("Bot", "MITM_PROXY")

    @cachetools.cached(cache)
    def fetch_proxy_data(self, url):
        proxy_pool = []
        for try_count in range(10):
            response = requests.get(url)
            if response.status_code == 200:
                json_data = response.json()
                for entry in json_data.get("data"):
                    proxy_pool.append(f"http://{entry['ip']}:{str(entry['port'])}")
                return proxy_pool
            else:
                time.sleep(5)

    def start(self, proxy=False, mitm=False):
        try:
            options = uc.ChromeOptions()
            if self._proxy is not None and proxy is True:
                proxy_pool = self.fetch_proxy_data(self._proxy)
                random_index = random.randint(0, len(proxy_pool) - 1)
                proxy = proxy_pool[random_index]
                options.add_argument(f"--proxy-server={proxy}")

            if self._mitm is not None and mitm is True:
                options.add_argument(f"--proxy-server={self._mitm}")

            if not self._debug:
                options.add_argument("--blink-settings=imagesEnabled=false")
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument('--no-sandbox')
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-web-security")
                options.add_argument("--disable-extensions")
                options.add_argument('--disable-application-cache')
                options.add_argument("--disable-setuid-sandbox")

            driver = uc.Chrome(
                               browser_executable_path='/usr/bin/chromium-browser',
                               driver_executable_path='/usr/bin/chromedriver', options=options,
                               )

            return driver
        except BaseException as e:
            print(f'webview开启失败{e}')
