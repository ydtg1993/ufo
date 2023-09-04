import threading
from controller.nytime import Nytime


class News:
    def __init__(self):
        thread1 = threading.Thread(target=Nytime)
        thread1.start()

        thread1.join()