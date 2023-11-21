import logging
import threading
import time
from datetime import datetime

from assiatant import GB
from assiatant.task_manager import TaskManager
from controller.detail import Detail
from controller.menu import Menu
from director.info import Info
from director.service import HttpService
from model.source_video_model import SourceVideoModel
from trans.video import TransVideo

T = TaskManager()
lock = threading.Lock()


def main():
    threading.Thread(target=HttpService).start()
    T.main_task_num(3)
    GB.redis.set_cache(GB.process_cache_conf['menu']['key'], 120)
    T.fill_task(process_menu, 300)
    T.fill_task(process_detail)
    T.fill_task(process_update_detail)
    T.fill_task(publish)
    T.dealing()


def process_menu():
    T.permanent_running(lambda: Menu(), '分类页列表', 600, 1200)


def process_detail():
    with lock:
        T.permanent_running(lambda: Detail(), '详情页信息', 30, 180)


def process_update_detail():
    with lock:
        T.permanent_running(lambda: Detail(True), '详情页信息重试', 300, 900)


def publish():
    T.permanent_running(lambda: TransVideo(), '发布', 3600 * 6, 3600 * 8)


def reset_comic_update_queue():
    while True:
        session = GB.mysql.connect()
        try:
            Info().insert_process('重置任务队列', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 3600 * 1)
            batch_size = 1000
            offset = 0
            tasks = GB.redis.get_queue(GB.process_cache_conf['detail.retry']['key'], 0, -1)
            while True:
                results = session.query(SourceVideoModel.id).filter(
                    SourceVideoModel.url == '').offset(offset).limit(batch_size).all()
                for result in results:
                    tasks.append(str(result[0]))
                tasks = list(set(tasks))
                offset += batch_size
                if len(results) < batch_size:
                    GB.redis.delete(GB.process_cache_conf['detail.retry']['key'])
                    for _, vid in enumerate(tasks):
                        GB.redis.enqueue(GB.process_cache_conf['detail.retry']['key'], vid)
                    break
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            session.close()
        time.sleep(3600 * 12)


if __name__ == '__main__':
    main()
