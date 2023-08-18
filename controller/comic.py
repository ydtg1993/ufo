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
        imgDownLoader = ImageDownloader("./resources", None, cookies)
        for comicElem in comicElems:
            comic = dict(source=3)
            tDom = comicElem.find_element(By.CLASS_NAME, "entry-title")
            comic["title"] = tDom.text.strip()
            comic["source_url"] = tDom.find_element(By.TAG_NAME,'a').get_attribute('href')
            comic["source_id"] = 0
            cover = comicElem.find_element(By.TAG_NAME, "img").get_attribute("data-src")
            comic["cover"] = imgDownLoader.download_image(cover)
            comic["label"] = '[]'
            comic["category"] = '[]'
            comic["source_data"] = comicElem.get_attribute('innerHTML')
            DB.insert_data('source_comic', comic)
