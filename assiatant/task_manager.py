import logging
import threading
import time
from datetime import datetime
from random import random

from assiatant.singleton import Singleton
from director.info import Info


@Singleton
class TaskManager:
    tasks = []
    messager = None

    def __init__(self, main_task_num: int):
        self.messager = Info()
        self.messager.set_stop_num(main_task_num)

    def fill_task(self, func, delay: int = 0):
        t = threading.Thread(target=func)
        t.start()
        self.tasks.append(t)
        if delay > 0:
            time.sleep(delay)

    def permanent_running(self, cls, task_title: str, st: int, ed: int):
        while True:
            try:
                self.messager.insert_process(task_title, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ed + 300)
                cls()
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))
            time.sleep(random.randint(st, ed))

    def dealing(self):
        for _, t in enumerate(self.tasks):
            t.join()
