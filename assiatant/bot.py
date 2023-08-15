import threading
import undetected_chromedriver as uc

class Bot(object):
    def __init__(self, n=1):
        self.Webdrivers = []
        self.BotThreads = []
        self.__workerNum = n
        for i in range(self.__workerNum):
            thread = threading.Thread(target=self.beginning, args=())
            self.BotThreads.append(thread)
            thread.start()

    def beginning(self):
        options = uc.ChromeOptions()
        options.add_argument("--load-images=no")
        driver = uc.Chrome(options=options, user_multi_procs=True)
        driver.get('https://baozimh.org/allmanga/')
        self.Webdrivers.append(driver)
