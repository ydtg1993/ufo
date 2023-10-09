import time
from selenium.webdriver.common.by import By
from assiatant import GB
from model.source_comic_model import SourceComicModel


class Menu:
    def __init__(self):
        self.url = "https://www.baozimh.com/"
        categories = {"恋爱": "lianai", "纯爱": "chunai"}
        regions = {"国漫": "cn", "韩漫": "kr"}

        for category_name in categories:
            for region_name in regions:
                self.scan_list({"name": category_name, "value": categories[category_name]},
                               {"name": region_name, "value": regions[region_name]})

    def scan_list(self, category: dict, region: dict):
        list_url = self.url + 'classify?type={category}&region={region}&state=all&filter=%2a'.format(
            category=category['value'], region=region['value'])
        url = "https://www.baozimh.com/"
        wb = GB.bot.start()
        wb.get(url)
        time.sleep(5)

        wb.get(list_url)
        time.sleep(3)
        repeat_signal = 0
        while True:
            if repeat_signal > 3:
                break

            wb.execute_script("window.scrollTo({'left':0,'top': 10000000,behavior: 'smooth'})")
            time.sleep(2)
            comic_doms = wb.find_elements(By.CSS_SELECTOR, 'div.comics-card')
            comic_doms.reverse()
            for _, comic_dom in enumerate(comic_doms):
                a = comic_dom.find_element(By.CSS_SELECTOR, "a:first-child")
                title = a.get_attribute('title')
                link = a.get_attribute('href')
                if GB.redis.get_hash(GB.config.get("Redis", "PREFIX") + "unique:comic:link", link) is not None:
                    repeat_signal += 1
                    break

                GB.redis.set_hash(GB.config.get("Redis", "PREFIX") + "unique:comic:link", link, "0")
                cover = a.find_element(By.TAG_NAME, "amp-img").get_attribute("src")

                print(title)
            time.sleep(2)
