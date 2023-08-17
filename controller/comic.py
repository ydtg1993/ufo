import time
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.downloader import ImageDownloader
from assiatant.proxy import Proxy
from assiatant.rd import RedisConnector
from configparser import ConfigParser


class Comic:
    def __init__(self, **kwargs):
        CONF: ConfigParser = kwargs.get('CONF')
        DB: MysqlConnector = kwargs.get('DB_POOL')
        RD: RedisConnector = kwargs.get('RD_POOL')
        BOT: Bot = kwargs.get('BOT_POOL')
        WB: Chrome = BOT.get_driver()

        url = CONF.get("App", "SOURCE_URL") + "/allmanga/"

        WB.get(f"{url}")
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, ".entries>article"))
        WebDriverWait(WB, 10).until(element_present)

        cookies = WB.get_cookies()
        time.sleep(5)
        comicElems = WB.find_elements(By.CSS_SELECTOR, ".entries>article")
        for comicElem in comicElems:
            print(comicElem.find_element(By.CLASS_NAME, "entry-title").text)
            cover = comicElem.find_element(By.TAG_NAME, "img").get_attribute("data-src")
            ImageDownloader("./resources", "", None, cookies).download_image(cover)
