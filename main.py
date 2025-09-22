import logging
import threading
import time
from datetime import datetime
from assiatant import GB
from assiatant.task_manager import TaskManager
from controller.chapter import Chapter
from controller.comic import Comic
from controller.page import Page

T = TaskManager()
lock = threading.Lock()


def main():
    #threading.Thread(target=HttpService).start()
    T.main_task_num(3)
    #T.fill_task(process_page, 300)
    #T.fill_task(process_comic)
    T.fill_task(process_chapter)
    #T.fill_task(publish)
    T.dealing()


def process_page():
    T.permanent_running(lambda: Page(), '分类页列表', 600, 1200)


def process_comic():
    with lock:
        T.permanent_running(lambda: Comic(), '详情页信息', 30, 180)


def process_chapter():
    with lock:
        T.permanent_running(lambda: Chapter(), '详情页信息重试', 300, 900)


if __name__ == '__main__':
    main()
