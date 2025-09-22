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


class Chapter:
    session = None

    def __init__(self, is_update=False):
        self.session = GB.mysql.connect()
        wb = GB.bot.retry_start(GB.config.get("App", "URL"), proxy=False, mitm=True, image=True)
        try:
            for _ in range(1000):
                task = GB.redis.dequeue(GB.process_cache_conf['chapters']['key'])
                if task is None:
                    break
                task = json.loads(task)
                comic_detail = self.session.query(SourceComicModel).filter(
                    SourceComicModel.id == task['comic_id']).first()
                if comic_detail is None:
                    continue
                wb.get(task['chapter_link'])
                self.smooth_scroll_to_bottom(wb)
                image_doms = wb.find_elements(By.CSS_SELECTOR, '.comicContent-list img')
                images = []
                for _, image_dom in enumerate(image_doms):
                    images.append(image_dom.get_attribute('data-src'))
                chapter_detail = SourceChapterModel(title=task['chapter_title'],
                                                    comic_id=comic_detail.id,
                                                    source_url=task['chapter_link'],
                                                    sort=comic_detail.chapter_count_download,
                                                    )
                comic_detail.chapter_count_download += 1
                self.session.add(chapter_detail)
                self.session.flush()
                if images:  # 如果有图片才创建记录
                    image_model = SourceImageModel(
                        comic_id=comic_detail.id,
                        chapter_id=chapter_detail.id,
                    )
                    image_model.set_images(images)
                    self.session.add(image_model)
                self.session.flush()
            self.session.commit()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            wb.quit()
            self.session.close()

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
