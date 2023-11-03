import json
import logging
import random
import re
import time
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome
from assiatant import GB
from datetime import datetime, timedelta


class Menu:
    total_page = 0
    page = 10

    def __init__(self):
        wb = GB.bot.retry_start(GB.config.get("App", "URL"))
        try:
            cache_key = GB.process_cache_conf['menu']['key']
            if GB.redis.get_cache(cache_key) is None:
                GB.redis.set_cache(cache_key, 528)
            p = GB.redis.get_cache(cache_key)
            wb.get(GB.config.get("App", "URL") + 'allmanga/page/{p}/'.format(p=p))
            self.total_page = int(p)
            self.browser(wb)
            GB.redis.set_cache(cache_key, self.total_page)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        wb.quit()

    def browser(self, wb: Chrome):
        while True:
            if self.page < 0:
                break
            if wb.current_url is GB.config.get("App", "URL") + 'allmanga/':
                break
            self.page -= 1
            self.total_page -= 1
            time.sleep(random.randint(5, 15))
            comic_doms = wb.find_elements(By.CSS_SELECTOR, 'div.entries>article>a')
            for _, comic_dom in enumerate(comic_doms):
                title = comic_dom.get_attribute('aria-label')
                link = comic_dom.get_attribute('href')
                if GB.redis.get_hash(GB.process_cache_conf['comic.unique']['key'], link) is not None:
                    continue

                GB.redis.set_hash(GB.process_cache_conf['comic.unique']['key'], link, "0")
                cover = comic_dom.find_element(By.CSS_SELECTOR, "a img").get_attribute("data-src")
                GB.redis.enqueue(GB.process_cache_conf['comic']['key'],
                                 json.dumps(
                                     {"title": title, "link": link, "cover": cover}))
            wb.execute_script("document.querySelector('nav.ct-pagination .prev').click();")
