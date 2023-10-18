import json
import logging
import random
import time
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome
from assiatant import GB
from datetime import datetime, timedelta


class Menu:
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

        num_per_group = 6
        category_groups = [categories[i:i + num_per_group] for i in range(0, len(categories), num_per_group)]
        try:
            wb = GB.bot.start()
            for region in regions:
                for category_group in category_groups:
                    try:
                        wb.get(GB.config.get("App", "URL"))
                        for category in category_group:
                            self.scan_list(wb, category, region)
                    except Exception as e:
                        logger = logging.getLogger(__name__)
                        logger.error(json.dumps({'message': e, 'args': e.args, 'traceback': e.__traceback__}))
            wb.quit()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(json.dumps({'message': e, 'args': e.args, 'traceback': e.__traceback__}))

    def scan_list(self, wb: Chrome, category: dict, region: dict):
        time.sleep(random.randint(7, 15))
        list_url = GB.config.get("App", "URL") + 'classify?type={category}&region={region}&state=all&filter=%2a'.format(
            category=category['value'], region=region['value'])
        unique_key = category['value'] + region['value']
        if unique_key not in GB.menu_tick:
            wb.switch_to.new_window()
            wb.get(list_url)
            GB.menu_tick[unique_key] = {"start": 0, "repeat": 5, "time": datetime.now()}
        now = datetime.now()
        if now - GB.menu_tick[unique_key]['time'] > timedelta(hours=72):
            GB.menu_tick[unique_key] = {"start": 0, "repeat": 5, "time": now}

        limit = 1
        while True:
            if GB.menu_tick[unique_key]["repeat"] < 0:
                break
            if GB.menu_tick_limit < limit:
                break
            limit += 1

            if GB.menu_tick[unique_key]['start'] > 0:
                for _ in range(GB.menu_tick[unique_key]['start']):
                    wb.execute_script(
                        "window.scrollTo({'left':0,'top': document.body.scrollHeight,behavior: 'smooth'})")
                    time.sleep(random.randint(6, 12))
                    is_bottom = wb.execute_script(
                        "return (window.innerHeight + window.scrollY >= document.body.scrollHeight - 2);")
                    if is_bottom is True:
                        break
            else:
                wb.execute_script("window.scrollTo({'left':0,'top': document.body.scrollHeight,behavior: 'smooth'})")
            time.sleep(random.randint(3, 9))
            comic_doms = wb.find_elements(By.CSS_SELECTOR, 'div.comics-card')
            comic_doms.reverse()
            for _, comic_dom in enumerate(comic_doms):
                a = comic_dom.find_element(By.CSS_SELECTOR, "a:first-child")
                title = a.get_attribute('title')
                link = a.get_attribute('href')
                if GB.redis.get_hash(GB.config.get("App", "PROJECT") + ":unique:comic:link", link) is not None:
                    GB.menu_tick[unique_key]["repeat"] -= 1
                    break

                GB.redis.set_hash(GB.config.get("App", "PROJECT") + ":unique:comic:link", link, "0")
                cover = a.find_element(By.TAG_NAME, "amp-img").get_attribute("src")
                GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":comic:task",
                                 json.dumps(
                                     {"title": title, "link": link, "cover": cover, "category": category['name'],
                                      "region": region['name']}))
        wb.switch_to.window(wb.window_handles[0])
        GB.menu_tick[unique_key]['start'] += GB.menu_tick_limit
