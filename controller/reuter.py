import time
from selenium.webdriver.common.by import By
from assiatant.globe import GB
import re

class Reuter:
    def __init__(self):
        self.db = GB['mysql']
        self.config = GB['config']
        self.rd = GB["redis"]
        self.wb = GB['bot'].get_pool()
        self.url = "https://www.reuters.com"

        self.wb.get(self.url)
        time.sleep(3)
        try:
            self.login()

            task_map = {}
            t0 = self.wb.find_elements(By.CSS_SELECTOR, "ul.home-page-grid__left-col__2K7_S a")
            self.fill_task(task_map,t0)

            t0[0].click()

        except BaseException as e:
            print(e)
        GB['bot'].return_pool(self.wb)

    @staticmethod
    def fill_task(task_map,doms):
        for t in doms:
            title = t.text
            if title == '' :continue
            link = t.get_attribute("href")
            task_map[title] = link

    def login(self):
        btn = self.wb.find_element(By.CLASS_NAME,"site-header__button-group__5IlZj")
        btnHtml = btn.get_attribute("innerHTML")
        if re.compile(r'hk').search(btnHtml):
            return

        self.wb.get(f"{self.url}/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2F")
        time.sleep(3)
        self.wb.find_element(By.CSS_SELECTOR, 'input#email').send_keys("ydtg19930330@gmail.com")
        time.sleep(1)
        self.wb.find_element(By.CSS_SELECTOR, 'input#password').send_keys("Susanoo&87350100")
        time.sleep(1)
        self.wb.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)