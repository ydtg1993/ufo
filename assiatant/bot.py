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
            
            driver = uc.Chrome(options=options,headless=True,debug=True,browser_executable_path="/usr/bin/google-chrome")
            return driver
        except BaseException as e:
            print(f'webview开启失败{e}')
