import time
from selenium.webdriver.common.by import By
from assiatant import GB
from model.source_comic_model import SourceComicModel


class Menu:
    def __init__(self):
        config = GB.config
        wb = GB.bot.start()
        url = config.get("App", "SOURCE_URL")

        wb.get(url + "/allmanga/")

        cookies = wb.get_cookies()
        combined_cookies = {}
        for cookie in cookies:
            combined_cookies[cookie["name"]] = cookie["value"]

        time.sleep(5)
