import logging
import random
import re
import time
from selenium.webdriver.common.by import By
from assiatant import GB
import json
from director.info import Info
from model.source_video_model import SourceVideoModel


class Detail:
    session = None

    def __init__(self):
        self.session = GB.mysql.connect()
        wb = GB.bot.retry_start(GB.config.get("App", "URL"))
        try:
            self.insert_process(wb)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            wb.quit()
            self.session.close()

    def insert_process(self, wb):
        for _ in range(12):
            i = Info()
            i.check_stop_signal()
            try:
                task = GB.redis.dequeue(GB.process_cache_conf['detail']['key'])
                if task is None:
                    time.sleep(random.randint(900, 1200))
                    break
                task = json.loads(task)
                time.sleep(random.randint(7, 30))
                title = task['title']
                link = task['link']
                i.insert_current_task('img', f'详情导入《{title}》-{link}')
                exist = self.session.query(SourceVideoModel).filter(
                    SourceVideoModel.source_url == task['link']).first()
                if exist is not None:
                    continue
                wb.get(task['link'])
                if not re.match(r'.*class="de-info-wr".*',
                                wb.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'),
                                re.DOTALL):
                    continue

                comic_id = self.comic_info(wb, task)
                if comic_id:
                    self.comic_chapter(wb, comic_id)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))

    def comic_info(self, wb, task):
        exist = self.session.query(SourceComicModel).filter(SourceComicModel.source_url == task['link']).first()
        if exist is not None:
            return
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
        comic = SourceComicModel(title=task['title'],
                                 source_url=task['link'],
                                 source=1,
                                 cover=task['cover'],
                                 region=task['region'],
                                 category=task['category'],
                                 label=json.dumps(tags),
                                 is_finish=is_finish,
                                 description=description,
                                 author=author)
        self.session.add(comic)
        self.session.commit()
        return comic.id
