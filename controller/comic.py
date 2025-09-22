import logging
import random
import re
import time
from selenium.webdriver.common.by import By
from assiatant import GB
import json

from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel
from model.source_img_model import SourceImageModel


class Comic:
    session = None

    def __init__(self, is_update=False):
        self.session = GB.mysql.connect()
        wb = GB.bot.retry_start(GB.config.get("App", "URL"), proxy=False, mitm=True, image=True)
        try:
            self.insert_process(wb)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            wb.quit()
            self.session.close()

    def insert_process(self, wb):
        for _ in range(50):
            try:
                task = GB.redis.dequeue(GB.process_cache_conf['comics']['key'])
                if task is None:
                    time.sleep(random.randint(100, 300))
                    break
                task = json.loads(task)
                title = task['title']
                link = task['link']
                cover = task['cover']
                wb.get(link)
                self.smooth_scroll_to_bottom(wb)
                exist = self.session.query(SourceComicModel).filter(
                    SourceComicModel.source_url == task['link']).first()
                if exist is not None:
                    continue
                author = wb.find_element(By.CSS_SELECTOR,
                                         '.container .comicParticulars-title-right li:nth-child(3) a').text
                publish_time = wb.find_element(By.CSS_SELECTOR,
                                               '.container .comicParticulars-title-right li:nth-child(5) > span.comicParticulars-right-txt').text
                description = wb.find_element(By.CSS_SELECTOR, '.intro').text
                tag_doms = wb.find_elements(By.CSS_SELECTOR, '.comicParticulars-tag>a')
                labels = []
                for _, tag_dom in enumerate(tag_doms):
                    labels.append(tag_dom.text)
                comic_detail = SourceComicModel(title=title,
                                                source=1,
                                                source_url=link,
                                                cover=cover,
                                                author=author,
                                                label=json.dumps(labels),
                                                category=labels[0] if labels else None,
                                                description=description,
                                                )
                chapter_link_doms = wb.find_elements(By.CSS_SELECTOR, '#default全部 a')
                self.session.add(comic_detail)
                self.session.flush()
                for _, chapter_link_dom in enumerate(chapter_link_doms):
                    chapter_link = chapter_link_dom.get_attribute('href')
                    chapter_title = chapter_link_dom.get_attribute('title')
                    if chapter_title != "":
                        GB.redis.enqueue(GB.process_cache_conf['chapters']['key'],
                                         json.dumps({"chapter_title": chapter_title, "chapter_link": chapter_link,
                                                     "comic_id": comic_detail.id}))
                comic_detail.chapter_count = len(chapter_link_doms)
                self.session.commit()
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))

    def smooth_scroll_to_bottom(self, wb, total_duration=5):
        # 获取初始的滚动高度
        last_height = wb.execute_script("return document.body.scrollHeight")
        # 计算每次滚动的小间隔时间（秒），这里取0.05秒，可以根据需要调整
        scroll_step_time = 0.05
        # 计算总共需要滚动的步数
        total_steps = int(total_duration / scroll_step_time)
        # 计算每步滚动的像素距离
        scroll_distance_per_step = last_height / total_steps

        current_position = 0
        for i in range(total_steps):
            # 计算下一次滚动的位置
            current_position += scroll_distance_per_step
            # 执行滚动 JavaScript
            wb.execute_script(f"window.scrollTo(0, {current_position});")
            # 等待一小段时间，模拟平滑滚动
            time.sleep(scroll_step_time)
        # 确保最终滚动到底部
        wb.execute_script("window.scrollTo(0, document.body.scrollHeight);")
