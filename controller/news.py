import threading
from controller.nytime import Nytime
from controller.reuter import Reuter


class News:
    def __init__(self):
        threads = []
        for _ in range(1):
            thread = threading.Thread(target=Reuter)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

