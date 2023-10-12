import json
import time
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome
from assiatant import GB
from model.source_comic_model import SourceComicModel


class Menu:
    Windows = {}

    def __init__(self):
        categories = [
            {"name": "恋爱", "value": "lianai"},
            {"name": "纯爱", "value": "chunai"}
        ]
        regions = [
            {"name": "国漫", "value": "cn"},
            {"name": "韩漫", "value": "kr"}
        ]

        for region in regions:
            wb = GB.bot.start()
            wb.get(GB.config.get("App", "URL"))
            time.sleep(5)
            for category in categories:
                self.scan_list(wb, category, region)
            self.Windows = {}
            wb.quit()

    def scan_list(self, wb: Chrome, category: dict, region: dict):
        list_url = GB.config.get("App", "URL") + 'classify?type={category}&region={region}&state=all&filter=%2a'.format(
            category=category['value'], region=region['value'])
        if category['value'] not in self.Windows:
            wb.window_new()
            wb.get(list_url)
            self.Windows[category['value']] = {"handle": wb.current_window_handle, "limit": 5, "repeat": 10}
        else:
            handle = self.Windows[category['value']]["handle"]
            wb.switch_to.window(handle)

        limit = 1
        time.sleep(3)
        while True:
            if self.Windows[category['value']]["repeat"] < 0:
                break
            if self.Windows[category['value']]["limit"] < limit:
                break
            limit += 1

            wb.execute_script("window.scrollTo({'left':0,'top': document.body.scrollHeight,behavior: 'smooth'})")
            time.sleep(3)
            comic_doms = wb.find_elements(By.CSS_SELECTOR, 'div.comics-card')
            comic_doms.reverse()
            for _, comic_dom in enumerate(comic_doms):
                a = comic_dom.find_element(By.CSS_SELECTOR, "a:first-child")
                title = a.get_attribute('title')
                link = a.get_attribute('href')
                if GB.redis.get_hash(GB.config.get("Redis", "PREFIX") + "unique:comic:link", link) is not None:
                    self.Windows[category['value']]["repeat"] -= 1
                    break

                GB.redis.set_hash(GB.config.get("Redis", "PREFIX") + "unique:comic:link", link, "0")
                cover = a.find_element(By.TAG_NAME, "amp-img").get_attribute("src")
                GB.redis.enqueue(GB.config.get("Redis", "PREFIX") + "comic:task",
                                 json.dumps(
                                     {"title": title, "link": link, "cover": cover, "category": category['name'],
                                      "region": region['name']}))
