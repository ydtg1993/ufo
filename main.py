import logging
import random
import threading
import time
from assiatant import GB
from controller.comic import Comic
from controller.img import Img
from controller.menu import Menu
from director.info import Info
from director.service import HttpService
from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel
from datetime import datetime

tt = []
i = Info()

def main():
    i.stop_task_num = 3
    threading.Thread(target=HttpService).start()
    fill_task(process_menu)
    time.sleep(3)

    fill_task(process_comic)
    time.sleep(3)

    fill_task(process_img)
    time.sleep(3)

    fill_task(process_update_comic)
    fill_task(reset_comic_update_queue)
    fill_task(reset_chapter_img_queue)

    for _, t in enumerate(tt):
        t.join()


def fill_task(func):
    t = threading.Thread(target=func)
    t.start()
    tt.append(t)


def process_menu():
    while True:
        try:
            i.insert_process('分类页列表', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 3600)
            Menu()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        time.sleep(random.randint(900, 3600))


def process_comic():
    while True:
        try:
            i.insert_process('漫画详情页', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 420)
            Comic()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        time.sleep(random.randint(120, 420))


def process_img():
    while True:
        try:
            i.insert_process('章节图片页', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 420)
            Img()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        time.sleep(random.randint(60, 420))


def process_update_comic():
    while True:
        try:
            i.insert_process('漫画章节更新', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1800)
            Comic(True)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        time.sleep(random.randint(600, 1800))


def reset_comic_update_queue():
    while True:
        try:
            i.insert_process('重置漫画更新队列', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 3600*9)
            batch_size = 500
            offset = 0
            tasks = GB.redis.get_queue(GB.config.get("App", "PROJECT") + ":chapter:task", 0, -1)
            while True:
                results = GB.mysql.session.query(SourceComicModel.id).filter(
                    SourceComicModel.source_chapter_count != SourceComicModel.chapter_count).offset(offset).limit(
                    batch_size).all()
                for result in results:
                    tasks.append(str(result[0]))
                tasks = list(set(tasks))
                offset += batch_size
                if len(results) < batch_size:
                    GB.redis.delete(GB.config.get("App", "PROJECT") + ":chapter:task")
                    for _, comic_id in enumerate(tasks):
                        GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":chapter:task", comic_id)
                    break
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        time.sleep(3600*9)


def reset_chapter_img_queue():
    while True:
        try:
            i.insert_process('重置章节图片抓取队列', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 3600 * 6)
            batch_size = 500
            offset = 0
            tasks = GB.redis.get_queue(GB.config.get("App", "PROJECT") + ":img:task", 0, -1)
            while True:
                results = GB.mysql.session.query(SourceChapterModel.id).filter(
                    SourceChapterModel.img_count == 0).offset(offset).limit(
                    batch_size).all()
                for result in results:
                    tasks.append(str(result[0]))
                tasks = list(set(tasks))
                offset += batch_size
                if len(results) < batch_size:
                    GB.redis.delete(GB.config.get("App", "PROJECT") + ":img:task")
                    for _, chapter_id in enumerate(tasks):
                        GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":img:task", chapter_id)
                    break
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        time.sleep(3600 * 6)


if __name__ == '__main__':
    main()
