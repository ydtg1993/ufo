import json
import logging
import random
import time
from selenium.webdriver.common.by import By
from assiatant import GB


class Menu:
    def __init__(self):
        wb = GB.bot.start(GB.config.get("App", "URL"))
        page = 179
        while True:
            if page <= 0:
                break
            url = GB.config.get("App", "URL") + 'vod/show/by/hits/id/{page}/'.format(page=page)
            wb.get(url)
            page -= 1
            boxes = wb.find_elements(By.CSS_SELECTOR, 'div.list>ul li')
            for _, box in enumerate(boxes):
                cover = box.find_element(By.TAG_NAME, 'img').get_attribute('src')
                a = box.find_element(By.CSS_SELECTOR, 'p.name>a')
                link = a.get_attribute('href')
                title = a.text
                if GB.redis.get_hash(GB.process_cache_conf['av.unique']['key'], link) is not None:
                    continue
                GB.redis.enqueue(GB.process_cache_conf['detail']['key'],
                                 json.dumps({"title": title, "link": link, "cover": cover}))
                GB.redis.set_hash(GB.process_cache_conf['av.unique']['key'], link, "0")
            time.sleep(random.randint(3, 5))
        wb.quit()
