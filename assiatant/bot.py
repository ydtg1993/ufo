from configparser import ConfigParser
import undetected_chromedriver as uc


class Bot(object):
    def __init__(self, config: ConfigParser):
        self.DEBUG = bool(config.get("App", "DEBUG"))

    def start(self):
        try:
            options = uc.ChromeOptions()
            if not self.DEBUG:
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
