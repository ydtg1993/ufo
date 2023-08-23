import configparser
import json
import random
import time
import requests
import undetected_chromedriver as uc
from configparser import ConfigParser
from assiatant.rd import RedisConnector


class Bot(object):
    _debug = None
    _proxy = None

    def __init__(self, config: ConfigParser):
        self._debug = True if config.get("App", "DEBUG") == 'on' else False

    def proxy(self,config:configparser,rd:RedisConnector):
        save_data = []
        proxy = ""
        cache = "proxy:" + config.get("Bot", "PROXY_URL")
        cache_proxy = rd.get_cache(cache)
        if cache_proxy:
            try:
                save_data = json.loads(cache_proxy)
                if save_data:
                    random_index = random.randint(0, len(save_data) - 1)
                    return save_data[random_index]
            except Exception as e:
                raise e

        for try_count in range(10):
            response = requests.get(GB['config'].get("Bot", "PROXY_URL"))
            if response.status_code == 200:
                json_data = response.json()
                for entry in json_data.get("data"):
                    save_data.append(f"http://{entry['ip']}:{str(entry['port'])}")
                break
            else:
                time.sleep(5)

        if len(save_data) > 0:
            random_index = random.randint(0, len(save_data) - 1)
            proxy = save_data[random_index]
            rd.set_cache(cache, json.dumps(save_data))
        self._proxy = proxy

    def start(self):
        try:
            options = uc.ChromeOptions()
            if not self._proxy :
                options.add_argument(f"--proxy-server={self._proxy}")
                self._proxy = None

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

            driver = uc.Chrome(options=options)
            return driver
        except BaseException as e:
            print(f'webview开启失败{e}')
