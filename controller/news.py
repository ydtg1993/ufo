import threading
from controller.nytime import Nytime
from controller.reuter import Reuter


class News:
    def __init__(self):
        ReuterThreads = []
        for _ in range(2):
            thread = threading.Thread(target=Reuter)
            ReuterThreads.append(thread)
            thread.start()

        for thread in ReuterThreads:
            thread.join()

