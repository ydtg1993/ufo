import time
from controller.comic import Comic
from controller.img import Img
from controller.menu import Menu
import threading
import sys

def main():
    args = sys.argv
    if args[1] == 'menu':
        Menu()
        return
    
    t2 = threading.Thread(target=deal_comic)
    t2.start()
    time.sleep(3)

    t3 = threading.Thread(target=deal_img)
    t3.start()

    t2.join()
    t3.join()


def deal_comic():
    while True:
        Comic()
        time.sleep(120)


def deal_img():
    while True:
        Img()
        time.sleep(90)


if __name__ == '__main__':
    main()
