import sys
import cachetools
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager  # 导入 GeckoDriverManager
from configparser import ConfigParser


class Bot(object):
    _debug = None
    _proxy = None
    _mitm = None
    _browser_path = None
    cache = cachetools.TTLCache(maxsize=100, ttl=800)

    def __init__(self, config: ConfigParser):
        self._debug = True if config.get("App", "DEBUG") == 'on' else False
        if config.get("Bot", "PROXY_URL"):
            self._proxy = config.get("Bot", "PROXY_URL")
        if config.get("Bot", "MITM_PROXY"):
            self._mitm = config.get("Bot", "MITM_PROXY")
        if config.get("Bot", "BROWSER_PATH"):
            self._browser_path = config.get("Bot", "BROWSER_PATH")

        # 移除 GECKODRIVER_PATH 的配置检查，因为 webdriver-manager 会自动处理

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

    def start(self, proxy=False, mitm=False, image=False) -> webdriver.Firefox:
        try:
            options = Options()

            # 如果配置中指定了 Firefox 可执行文件路径，则设置 binary_location
            if self._browser_path:
                options.binary_location = self._browser_path

            # 代理设置
            if self._proxy is not None and proxy is True:
                proxy_pool = self.fetch_proxy_data(self._proxy)
                if proxy_pool:
                    random_index = random.randint(0, len(proxy_pool) - 1)
                    proxy_addr = proxy_pool[random_index]
                    options.set_preference('network.proxy.type', 1)
                    options.set_preference('network.proxy.http', proxy_addr.split('://')[1].split(':')[0])
                    options.set_preference('network.proxy.http_port', int(proxy_addr.split(':')[2]))
                    options.set_preference('network.proxy.ssl', proxy_addr.split('://')[1].split(':')[0])
                    options.set_preference('network.proxy.ssl_port', int(proxy_addr.split(':')[2]))

            if self._mitm is not None and mitm is True:
                options.set_preference('network.proxy.type', 1)
                options.set_preference('network.proxy.http', self._mitm.split('://')[1].split(':')[0])
                options.set_preference('network.proxy.http_port', int(self._mitm.split(':')[2]))
                options.set_preference('network.proxy.ssl', self._mitm.split('://')[1].split(':')[0])
                options.set_preference('network.proxy.ssl_port', int(self._mitm.split(':')[2]))
                options.set_preference("security.enterprise_roots.enabled", True)

            options.set_preference('permissions.default.image', 2 if not self._debug and not image else 1)

            # 其他选项设置
            if not self._debug:
                options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

            # 设置一些额外的偏好设置以更好地模拟真实浏览器或避免检测
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference('useAutomationExtension', False)
            options.set_preference("general.useragent.override",
                                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0")

            # 使用 webdriver-manager 自动管理 geckodriver:cite[1]:cite[2]:cite[5]
            # 创建 Service 对象并使用 GeckoDriverManager 自动下载和管理驱动
            gecko_service = Service(executable_path=GeckoDriverManager().install())
            driver = webdriver.Firefox(service=gecko_service, options=options)

            driver.set_page_load_timeout(90)
            return driver
        except BaseException as e:
            print(f'Firefox 浏览器开启失败: {e}')
            raise

    def retry_start(self, url: str, **kwargs) -> webdriver.Firefox:
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                wb = self.start(**kwargs)
                wb.get(url)
                return wb
            except Exception as e:
                print(f"尝试 {attempt + 1} 失败: {e}")
                if 'wb' in locals() and wb is not None:
                    wb.quit()
                if attempt == max_attempts - 1:
                    raise Exception(f"Failed to initialize Firefox WebDriver after {max_attempts} attempts.")
                time.sleep(2)

        raise Exception("Failed to initialize WebDriver after {} attempts.".format(max_attempts))