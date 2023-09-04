import time
from selenium.webdriver.common.by import By
from assiatant.downloader import ImageDownloader
from assiatant.globe import GB
from model.cate_model import CateModel
from model.new_model import NewModel
import re
import pickle


class Reuter:
    def __init__(self):
        self.db = GB['mysql']
        self.config = GB['config']
        self.wb = GB['bot'].start()
        self.login()

    def login(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.wb.add_cookie(cookie)

        current_cookies = self.wb.get_cookies()

        self.wb.get("https://www.reuters.com/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2F")
        self.wb.find_element(By.CSS_SELECTOR, 'input#email').send_keys("ydtg19930330@gmail.com")
        time.sleep(1)
        self.wb.find_element(By.CSS_SELECTOR, 'input#password').send_keys("Susanoo&87350100")
        time.sleep(1)
        self.wb.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(7)
        pickle.dump(self.wb.get_cookies(), open("cookies.pkl", "wb"))