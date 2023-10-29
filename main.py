
import threading
from assiatant.task_manager import TaskManager
from controller.menu import Menu
from director.service import HttpService

T = TaskManager()


def main():
    threading.Thread(target=HttpService).start()
    T.main_task_num(3)
    T.fill_task(process_menu, 300)
    T.dealing()


def process_menu():
    T.permanent_running(lambda: Menu(), '分类页列表', 900, 3600)


if __name__ == '__main__':
    main()
