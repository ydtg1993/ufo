import logging
import random
import re
import time
from selenium.webdriver.common.by import By
from assiatant import GB
import json
from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel


class Comic:
    chapter_limit = 30

    def __init__(self, is_update=False):
        if random.random() < 0.5:
            wb = GB.bot.start()
        else:
            wb = GB.bot.start(proxy=True)

        try:
            wb.get(GB.config.get("App", "URL"))
            if is_update:
                self.update_process(wb)
            else:
                self.insert_process(wb)
            wb.quit()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))

    def insert_process(self, wb):
        for _ in range(12):
            try:
                task = GB.redis.dequeue(GB.config.get("App", "PROJECT") + ":comic:task")
                if task is None:
                    break
                task = json.loads(task)
                time.sleep(random.randint(7, 30))
                exist = GB.mysql.session.query(SourceComicModel).filter(
                    SourceComicModel.source_url == task['link']).first()
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

    def update_process(self, wb):
        for _ in range(12):
            try:
                comic_id = GB.redis.dequeue(GB.config.get("App", "PROJECT") + ":chapter:task")
                if comic_id is None:
                    break
                time.sleep(random.randint(7, 30))
                record = GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.id == comic_id).first()
                if record is None:
                    continue
                wb.get(record.source_url)
                if not re.match(r'.*class="de-info-wr".*',
                                wb.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'),
                                re.DOTALL):
                    continue
                info_dom = wb.find_element(By.CSS_SELECTOR, "div.de-info-wr")
                tag_doms = info_dom.find_elements(By.CSS_SELECTOR, "div.tag-list>span.tag")
                self.comic_chapter(wb, comic_id)
                if tag_doms[0].text != "連載中" and record.is_finish == 0:
                    record.is_finish = 1
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))

    def comic_info(self, wb, task):
        exist = GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.source_url == task['link']).first()
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
        GB.mysql.session.add(comic)
        GB.mysql.session.flush()
        return comic.id

    def comic_chapter(self, wb, comic_id):
        record = GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.id == comic_id).first()
        if record is None:
            return
        wb.get(record.source_url)
        chapter_dom = wb.find_element(By.CSS_SELECTOR, "div.comics-detail > div:nth-child(3)")
        if not re.match(r'.*class="pure-g".*', chapter_dom.get_attribute('innerHTML')):
            return

        if re.match(r'.*id="chapter-items".*', chapter_dom.get_attribute('innerHTML')):
            chapters = chapter_dom.find_elements(By.CSS_SELECTOR, "#chapter-items a")
            chapters.extend(chapter_dom.find_elements(By.CSS_SELECTOR, "#chapters_other_list a"))
            self.chapter_patch(comic_id, chapters)
        else:
            chapters = chapter_dom.find_elements(By.CSS_SELECTOR, ".pure-g a")
            chapters.reverse()
            self.chapter_patch(comic_id, chapters)
        record.source_chapter_count = len(chapters)
        record.chapter_count = GB.mysql.session.query(SourceChapterModel).filter(
            SourceChapterModel.comic_id == comic_id).count()

    def chapter_patch(self, comic_id, chapters):
        limit = 0
        try:
            for sort, chapter in enumerate(chapters):
                if limit > self.chapter_limit:
                    GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":chapter:task", comic_id)
                    break
                link = chapter.get_attribute('href')
                title = chapter.get_attribute('textContent')
                if GB.redis.get_hash(GB.config.get("App", "PROJECT") + ":unique:chapter:link:" + str(comic_id),
                                     link) is not None:
                    continue

                chapter = SourceChapterModel(title=title,
                                             comic_id=comic_id,
                                             source_url=link,
                                             images='[]',
                                             sort=sort)
                GB.mysql.session.add(chapter)
                GB.mysql.session.flush()
                GB.redis.set_hash(GB.config.get("App", "PROJECT") + ":unique:chapter:link:" + str(comic_id), link, "0")
                GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":img:task", chapter.id)
                limit += 1
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            GB.mysql.session.commit()
