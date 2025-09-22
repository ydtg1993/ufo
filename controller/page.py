import json
import logging
import random
import time
from selenium.webdriver.common.by import By
from assiatant import GB


class Page:
    def __init__(self):
        wb = GB.bot.retry_start(GB.config.get("App", "URL"), proxy=True, mitm=False, image=False)
        wb.get(GB.config.get("App", "URL") + 'topic/remenmanhua202507')

        boxes = wb.find_elements(By.CSS_SELECTOR, 'main > div.row > .col-6')
        for _, box in enumerate(boxes):
            img_dom = box.find_element(By.TAG_NAME, 'img')
            cover = img_dom.get_attribute('data-src')
            link = box.find_element(By.CSS_SELECTOR, '.twoLines>a').get_attribute('href')
            title = box.find_element(By.CSS_SELECTOR, '.twoLines').text
            if GB.redis.get_hash(GB.process_cache_conf['comics.unique']['key'], link) is not None:
                continue
            GB.redis.enqueue(GB.process_cache_conf['comics']['key'],
                             json.dumps({"title": title, "link": link, "cover": cover}))
            GB.redis.set_hash(GB.process_cache_conf['comics.unique']['key'], link, "0")
