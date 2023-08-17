import random
import time
from configparser import ConfigParser
import requests
import json
from assiatant.rd import RedisConnector


class Proxy:
    def __init__(self,rd: RedisConnector, config: ConfigParser):
        self.RD: RedisConnector = rd
        self.proxyUrl = config.get("App","PROXY_URL")

    def get_proxy(self):
        save_data = []
        proxy = ""
        cache = "proxy:" + self.proxyUrl
        cache_proxy = self.RD.getCache(cache)
        if cache_proxy:
            try:
                save_data = json.loads(cache_proxy)
                if save_data:
                    random_index = random.randint(0, len(save_data) - 1)
                    return save_data[random_index]
            except Exception as e:
                raise e

        for try_count in range(10):
            response = requests.get(self.proxyUrl)
            if response.status_code == 200:
                json_data = response.json()
                value = json_data.get("data")
                print(value)
                break
            else:
                time.sleep(5)

        if save_data:
            random_index = random.randint(0, len(save_data) - 1)
            proxy = save_data[random_index]

        return proxy
