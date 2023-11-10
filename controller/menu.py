import json
import logging
import random
import time
from selenium.webdriver.common.by import By
from assiatant import GB


class Menu:
    def __init__(self):
        cache_key = GB.process_cache_conf['menu']['key']
        if GB.redis.get_cache(cache_key) is None:
            GB.redis.set_cache(cache_key, 123)
        page = int(GB.redis.get_cache(cache_key))
        if page < 1:
            return
        wb = GB.bot.start()
        for _ in range(15):
            wb.get(GB.config.get("App", "URL") + 'page/{page}/?filter=most-viewed'.format(page=page))
            page -= 1
            if page < 1:
                GB.redis.set_cache(cache_key, 0)
                break
            time.sleep(random.randint(7, 15))
            boxes = wb.find_elements(By.CSS_SELECTOR, '#main article')
            for _, box in enumerate(boxes):
                img_dom = box.find_element(By.TAG_NAME, 'img')
                cover = img_dom.get_attribute('data-src')
                a = box.find_element(By.TAG_NAME, 'a')
                link = a.get_attribute('href')
                title = img_dom.get_attribute('alt')
                if GB.redis.get_hash(GB.process_cache_conf['av.unique']['key'], link) is not None:
                    continue
                GB.redis.enqueue(GB.process_cache_conf['detail']['key'],
                                 json.dumps({"title": title, "link": link, "cover": cover}))
                GB.redis.set_hash(GB.process_cache_conf['av.unique']['key'], link, "0")
            GB.redis.set_cache(cache_key, page)
        wb.quit()
