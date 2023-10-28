import threading

from assiatant.task_manager import TaskManager
from controller.nytime import Nytime
from controller.reuter import Reuter
from director.service import HttpService

T = TaskManager(3)


def main():
    threading.Thread(target=HttpService).start()
    T.fill_task(process_reuter, 300)
    T.fill_task(process_nytime)
    T.dealing()


def process_reuter():
    T.permanent_running(lambda: Reuter(), '路透社', 3600, 7200)


def process_nytime():
    T.permanent_running(lambda: Nytime(), '纽约时报', 3600, 7200)


if __name__ == '__main__':
    main()
