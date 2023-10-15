import json
import random
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
            {"name": "纯爱", "value": "chunai"},
            {"name": "古風", "value": "gufeng"},
            {"name": "異能", "value": "yineng"},
            {"name": "懸疑", "value": "xuanyi"},
            {"name": "劇情", "value": "juqing"},
            {"name": "科幻", "value": "kehuan"},
            {"name": "奇幻", "value": "qihuan"},
            {"name": "玄幻", "value": "xuanhuan"},
            {"name": "穿越", "value": "chuanyue"},
            {"name": "冒險", "value": "mouxian"},
            {"name": "推理", "value": "tuili"},
            {"name": "武俠", "value": "wuxia"},
            {"name": "格鬥", "value": "gedou"},
            {"name": "戰爭", "value": "zhanzheng"},
            {"name": "熱血", "value": "rexie"},
            {"name": "搞笑", "value": "gaoxiao"},
            {"name": "大女主", "value": "danuzhu"},
            {"name": "都市", "value": "dushi"},
            {"name": "總裁", "value": "zongcai"},
            {"name": "後宮", "value": "hougong"},
            {"name": "日常", "value": "richang"},
            {"name": "少年", "value": "shaonian"},
            {"name": "其它", "value": "qita"},
        ]
        regions = [
            {"name": "国漫", "value": "cn"},
            {"name": "日本", "value": "jp"},
            {"name": "韩漫", "value": "kr"}
        ]

        for category in categories:
            wb = GB.bot.start()
            wb.get(GB.config.get("App", "URL"))
            for region in regions:
                self.scan_list(wb, category, region)
            self.Windows = {}
            wb.quit()

    def scan_list(self, wb: Chrome, category: dict, region: dict):
        list_url = GB.config.get("App", "URL") + 'classify?type={category}&region={region}&state=all&filter=%2a'.format(
            category=category['value'], region=region['value'])
        if category['value'] not in self.Windows:
            wb.window_new()
            wb.switch_to.window(wb.window_handles[-1])
            wb.get(list_url)
            self.Windows[category['value']] = {"handle": wb.current_window_handle, "limit": 5, "repeat": 5}
        else:
            handle = self.Windows[category['value']]["handle"]
            wb.switch_to.window(handle)

        limit = 1
        time.sleep(5)
        while True:
            if self.Windows[category['value']]["repeat"] < 0:
                break
            if self.Windows[category['value']]["limit"] < limit:
                break
            limit += 1

            wb.execute_script("window.scrollTo({'left':0,'top': document.body.scrollHeight,behavior: 'smooth'})")
            time.sleep(random.randint(7, 15))
            comic_doms = wb.find_elements(By.CSS_SELECTOR, 'div.comics-card')
            comic_doms.reverse()
            for _, comic_dom in enumerate(comic_doms):
                a = comic_dom.find_element(By.CSS_SELECTOR, "a:first-child")
                title = a.get_attribute('title')
                link = a.get_attribute('href')
                if GB.redis.get_hash(GB.config.get("App", "PROJECT") + ":unique:comic:link", link) is not None:
                    self.Windows[category['value']]["repeat"] -= 1
                    break

                GB.redis.set_hash(GB.config.get("App", "PROJECT") + ":unique:comic:link", link, "0")
                cover = a.find_element(By.TAG_NAME, "amp-img").get_attribute("src")
                GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":comic:task",
                                 json.dumps(
                                     {"title": title, "link": link, "cover": cover, "category": category['name'],
                                      "region": region['name']}))
