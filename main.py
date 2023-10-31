import logging
import threading
import time
from assiatant import GB
from assiatant.task_manager import TaskManager
from controller.comic import Comic
from controller.img import Img
from controller.menu import Menu
from director.info import Info
from director.service import HttpService
from model.source_comic_model import SourceComicModel
from datetime import datetime

T = TaskManager()


def main():
    threading.Thread(target=HttpService).start()
    T.main_task_num(4)
    #T.fill_task(process_menu, 300)
    #T.fill_task(process_comic, 120)
    T.fill_task(process_img, 30)
    T.fill_task(process_img2, 30)
    T.fill_task(process_img3, 30)
    T.fill_task(process_update_comic)
    T.fill_task(reset_comic_update_queue)
    T.dealing()


def process_menu():
    T.permanent_running(lambda: Menu(), '分类页列表', 1200, 3600)


def process_comic():
    T.permanent_running(lambda: Comic(), '漫画详情页', 120, 420)


def process_img():
    T.permanent_running(lambda: Img(), '章节图片页', 15, 60)


def process_img2():
    T.permanent_running(lambda: Img(), '章节图片页-进程2', 15, 60)


def process_img3():
    T.permanent_running(lambda: Img(), '章节图片页-进程3', 15, 60)


def process_update_comic():
    T.permanent_running(lambda: Comic(True), '漫画章节更新', 600, 1800)


def reset_comic_update_queue():
    while True:
        session = GB.mysql.connect()
        try:
            Info().insert_process('重置漫画更新队列', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 3600 * 9)
            batch_size = 500
            offset = 0
            tasks = GB.redis.get_queue(GB.process_cache_conf['chapter']['key'], 0, -1)
            while True:
                results = session.query(SourceComicModel.id).filter(
                    SourceComicModel.source_chapter_count != SourceComicModel.chapter_count).offset(offset).limit(
                    batch_size).all()
                for result in results:
                    tasks.append(str(result[0]))
                tasks = list(set(tasks))
                offset += batch_size
                if len(results) < batch_size:
                    GB.redis.delete(GB.process_cache_conf['chapter']['key'])
                    for _, comic_id in enumerate(tasks):
                        GB.redis.enqueue(GB.process_cache_conf['chapter']['key'], comic_id)
                    break
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            session.close()
        time.sleep(3600 * 24)


if __name__ == '__main__':
    main()
