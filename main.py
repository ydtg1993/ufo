import threading
from assiatant.task_manager import TaskManager
from controller.detail import Detail
from controller.menu import Menu
from director.service import HttpService

T = TaskManager()

def main():
    threading.Thread(target=HttpService).start()
    T.main_task_num(2)
    T.fill_task(process_menu, 300)
    T.fill_task(process_detail)
    T.dealing()


def process_menu():
    T.permanent_running(lambda: Menu(), '分类页列表', 3600, 7200)


def process_detail():
    T.permanent_running(lambda: Detail(), '详情页信息', 15, 60)

if __name__ == '__main__':
    main()
