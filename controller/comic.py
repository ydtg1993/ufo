import time

from selenium.webdriver.common.by import By

from assiatant import GB
import json

from model.source_comic_model import SourceComicModel


class Comic:
    def __init__(self):
        wb = GB.bot.start()
        for _ in range(12):
            wb.get(GB.config.get("App", "URL"))
            time.sleep(3)

            task = GB.redis.dequeue(GB.config.get("Redis", "PREFIX") + "comic:task")
            if task is None:
                return
            task = json.loads(task)

            exist = GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.source_url == task['link']).first()
            if exist is not None:
                return
            wb.get(task['link'])
            info_dom = wb.find_element(By.CSS_SELECTOR, "div.de-info-wr")
            author = info_dom.find_element(By.CSS_SELECTOR, "h2.comics-detail__author").text
            description = info_dom.find_element(By.CSS_SELECTOR, "p.comics-detail__desc").text.strip()
            tag_doms = info_dom.find_elements(By.CSS_SELECTOR, "div.tag-list>span.tag")
            is_finish = 0
            tags = []
            for index, dom in enumerate(tag_doms):
                if index == 0:
                    if dom.text != "連載中":
                        is_finish = 1
                    continue
                elif index == 1:
                    continue
                tags.append(dom.text.strip())

        wb.quit()
