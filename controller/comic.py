import logging
import os
import random
import re
import time
from selenium.webdriver.common.by import By
from assiatant import GB
import json
from urllib.parse import urlparse
from director.info import Info
from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel


class Comic:
    chapter_limit = 30
    session = None

    def __init__(self, is_update=False):
        wb = GB.bot.retry_start(GB.config.get("App", "URL"))
        self.session = GB.mysql.connect()
        try:
            wb.get(GB.config.get("App", "URL"))
            if is_update:
                self.update_process(wb)
            else:
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
                task = GB.redis.dequeue(GB.process_cache_conf['comic']['key'])
                if task is None:
                    time.sleep(random.randint(300, 600))
                    break
                task = json.loads(task)
                time.sleep(random.randint(7, 15))
                title = task['title']
                link = task['link']
                i.insert_current_task('img', f'漫画导入《{title}》-{link}')
                if GB.redis.get_hash(GB.process_cache_conf['comic.unique']['key'],link) is not None:
                    continue
                wb.get(link)
                if not re.match(r'.*class="entry-content".*',
                                wb.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'),
                                re.DOTALL):
                    continue

                comic_id = self.comic_info(wb, task)
                if comic_id:
                    GB.redis.set_hash(GB.process_cache_conf['comic.unique']['key'], link, comic_id)
                    wb.get(GB.config.get("App", "URL") + 'chapterlist/' + urlparse(link).path.strip('/').split('/')[-1] + '.html')
                    self.comic_chapter(wb, comic_id)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))

    def update_process(self, wb):
        for _ in range(12):
            i = Info()
            i.check_stop_signal()
            try:
                comic_id = GB.redis.dequeue(GB.process_cache_conf['chapter']['key'])
                if comic_id is None:
                    break
                time.sleep(random.randint(7, 15))
                record = self.session.query(SourceComicModel).filter(SourceComicModel.id == comic_id).first()
                if record is None:
                    continue
                i.insert_current_task('img', f'漫画更新《{record.title}》-{comic_id}')
                wb.get(record.source_url)
                if not re.match(r'.*class="de-info-wr".*',
                                wb.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'),
                                re.DOTALL):
                    continue
                info_dom = wb.find_element(By.CSS_SELECTOR, "div.de-info-wr")
                if re.match(r'.*class="tag-list".*',
                            info_dom.get_attribute('innerHTML'),
                            re.DOTALL):
                    tag_doms = info_dom.find_elements(By.CSS_SELECTOR, "div.tag-list>span.tag")
                    if tag_doms[0].text != "連載中" and record.is_finish == 0:
                        record.is_finish = 1
                self.comic_chapter(wb, comic_id)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))

    def comic_info(self, wb, task):
        if self.session.query(SourceComicModel).filter(
                    SourceComicModel.source_url == task['link']).first() is not None:
            return
        author = wb.find_element(By.CSS_SELECTOR, "div.author-content>a").text
        region = wb.find_element(By.CSS_SELECTOR, "div.genres-content>a").text
        description = wb.find_element(By.CSS_SELECTOR, "p.stk-block-text__text").text.strip()
        is_finish = 0
        if wb.find_elements(By.CSS_SELECTOR, "div.author-content")[1].text != 'Status: OnGoing':
            is_finish = 1

        tag_doms = wb.find_elements(By.CSS_SELECTOR, "div.genres-content")[1].find_elements(By.TAG_NAME, "a")
        tags = []
        for index, dom in enumerate(tag_doms):
            tags.append(dom.text.strip())
        comic = SourceComicModel(title=task['title'],
                                 source_url=task['link'],
                                 source=1,
                                 cover=task['cover'],
                                 region=region,
                                 category=tags[0],
                                 label=json.dumps(tags),
                                 is_finish=is_finish,
                                 description=description,
                                 author=author)
        self.session.add(comic)
        self.session.commit()
        return comic.id

    def comic_chapter(self, wb, comic_id):
        record = self.session.query(SourceComicModel).filter(SourceComicModel.id == comic_id).first()
        if record is None:
            return
        chapters = wb.find_elements(By.CSS_SELECTOR, "a.wp-manga-chapterlist")
        chapters.reverse()
        self.chapter_patch(comic_id, chapters)
        record.source_chapter_count = len(chapters)
        record.chapter_count = self.session.query(SourceChapterModel).filter(
            SourceChapterModel.comic_id == comic_id).count()
        self.session.commit()

    def chapter_patch(self, comic_id, chapters):
        limit = 0
        try:
            for sort, chapter in enumerate(chapters):
                if limit > self.chapter_limit:
                    break
                link = chapter.get_attribute('href')
                title = chapter.get_attribute('textContent')
                if GB.redis.get_hash(GB.process_cache_conf['chapter.unique']['key'] + str(comic_id),
                                     link) is not None:
                    continue

                chapter = SourceChapterModel(title=title,
                                             comic_id=comic_id,
                                             source_url=link,
                                             images='[]',
                                             sort=sort)
                self.session.add(chapter)
                self.session.commit()
                GB.redis.set_hash(GB.process_cache_conf['chapter.unique']['key'] + str(comic_id), link, "0")
                GB.redis.enqueue(GB.process_cache_conf['img']['key'], chapter.id)
                limit += 1
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
