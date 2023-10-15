import random
import time
from selenium.webdriver.common.by import By
from assiatant import GB
import json
from model.source_comic_model import SourceComicModel


class Comic:
    def __init__(self):
        wb = GB.bot.start()
        wb.get(GB.config.get("App", "URL"))
        for _ in range(12):
            task = GB.redis.dequeue(GB.config.get("App", "PROJECT") + ":comic:task")
            if task is None:
                break
            task = json.loads(task)

            exist = GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.source_url == task['link']).first()
            if exist is not None:
                break
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

            i = SourceComicModel(title=task['title'],
                                 source_url=task['link'],
                                 source=3,
                                 cover=task['cover'],
                                 region=task['region'],
                                 category=task['category'],
                                 label=json.dumps(tags),
                                 is_finish=is_finish,
                                 description=description,
                                 author=author).insert()
            GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":chapter:task", i)
            time.sleep(random.randint(7, 15))
        wb.quit()
