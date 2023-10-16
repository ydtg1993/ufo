import time
from controller.chapter import Chapter
from controller.comic import Comic
from controller.img import Img
from controller.menu import Menu
import threading


def main():
    t1 = threading.Thread(target=Menu)
    t1.daemon = True
    t1.start()
    time.sleep(600)

    t2 = threading.Thread(target=deal_comic)
    t2.daemon = True
    t2.start()
    time.sleep(300)

    t3 = threading.Thread(target=deal_chapter)
    t3.daemon = True
    t3.start()
    time.sleep(60)

    t4 = threading.Thread(target=deal_img)
    t4.daemon = True
    t4.start()


def deal_comic():
    while True:
        Comic()
        time.sleep(30)


def deal_chapter():
    while True:
        Chapter()
        time.sleep(30)


def deal_img():
    while True:
        Img()
        time.sleep(30)


if __name__ == '__main__':
    main()
