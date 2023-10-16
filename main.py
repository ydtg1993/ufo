import time
from controller.comic import Comic
from controller.img import Img
from controller.menu import Menu
import threading


def main():
    # t1 = threading.Thread(target=Menu)
    # t1.daemon = True
    # t1.start()
    # time.sleep(600)
    deal_comic()
    t2 = threading.Timer(300, deal_comic)
    t2.daemon = True
    t2.start()

    t3 = threading.Timer(360, deal_img)
    t3.daemon = True
    t3.start()

    t2.join()
    t3.join()


def deal_comic():
    Comic()


def deal_img():
    Img()


if __name__ == '__main__':
    main()
