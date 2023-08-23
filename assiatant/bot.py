from configparser import ConfigParser
import undetected_chromedriver as uc


class Bot(object):
    def __init__(self, config: ConfigParser):
        num = int(config.get("Bot", "thread"))

    def start(self):
        try:
            options = uc.ChromeOptions()
            options.add_argument('--incognito')
            options.add_argument("--start-maximized")
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument("--disable-extensions")
            options.add_argument('--disable-application-cache')
            options.add_argument('--disable-gpu')
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-setuid-sandbox")
            driver = uc.Chrome(options=options,browser_executable_path="/usr/bin/google-chrome")
            return driver
        except BaseException as e:
            print(f'webview开启失败{e}')
