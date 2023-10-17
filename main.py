import random
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
    
    t1 = threading.Thread(target=process_comic)
    t1.start()
    time.sleep(5)

    t2 = threading.Thread(target=process_img)
    t2.start()
    time.sleep(5)

    t3 = threading.Thread(target=process_update_comic)
    t3.start()

    t1.join()
    t2.join()
    t3.join()


def process_comic():
    while True:
        Comic()
        time.sleep(random.randint(60, 240))


def process_img():
    while True:
        Img()
        time.sleep(random.randint(30, 240))


def process_update_comic():
    while True:
        Comic(True)
        time.sleep(random.randint(60, 300))


if __name__ == '__main__':
    main()
