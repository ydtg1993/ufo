from configparser import ConfigParser
import undetected_chromedriver as uc


class Bot(object):
    def __init__(self, config: ConfigParser):
        num = int(config.get("Bot", "thread"))

    def start(self):
        try:
            options = uc.ChromeOptions()
            options.add_argument("window-size=1920,1080")
            options.add_argument('--blink-settings=imagesEnabled=false')
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            options.add_argument(f'user-agent={user_agent}')
            driver = uc.Chrome(options=options,headless=True,debug=True)
            return driver
        except BaseException as e:
            print(f'webview开启失败{e}')
