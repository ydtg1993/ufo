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
    page_limit = 5

    def __init__(self):
        wb = GB.bot.retry_start(GB.config.get("App", "URL"))
        try:
            wb.get(GB.config.get("App", "URL") + 'allmanga/page/528/')
            self.browser(wb)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        wb.quit()

    def browser(self, wb: Chrome):
        while True:
            nav_dom = wb.find_element(By.CSS_SELECTOR, 'nav.ct-pagination')
            if not re.match(r'.*class="next page-numbers".*',
                            nav_dom.get_attribute('innerHTML'),
                            re.DOTALL):
                break

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
