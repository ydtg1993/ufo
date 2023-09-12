import threading

from assiatant.globe import GB
from controller.nytime import Nytime
from controller.reuter import Reuter


class News:
    def __init__(self):
        threads = []
        for _ in range(1):
            if GB["config"].get('App', 'PROJECT') == 'nytime':
                thread = threading.Thread(target=Nytime)
            else:
                thread = threading.Thread(target=Reuter)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

