import threading
from controller.nytime import Nytime
from controller.reuter import Reuter


class News:
    def __init__(self):
        #thread1 = threading.Thread(target=Nytime)
        thread2 = threading.Thread(target=Reuter)

        #thread1.start()
        thread2.start()

        #thread1.join()
        thread2.join()