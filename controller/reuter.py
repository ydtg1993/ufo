import time
from selenium.webdriver.common.by import By
from assiatant.globe import GB
import re

class Reuter:
    type_list = {
        "World":22,
        "Technology":29,
        "Business":18,
        "Retail & Consumer":18,
        "Markets": 18,
        "Insight": 18,
        "Charged":23,
        "Americas":24,
        "United States":24,
        "Lifestyle":32,
    }

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
            self.wb.execute_script('''
            window.scrollTo({top: 10000000,behavior: 'smooth'});
                ''')
            time.sleep(2)
            task_map = {}

            t0 = self.wb.find_elements(By.CSS_SELECTOR, 'ul.home-page-grid__left-col__2K7_S a[data-testid="Heading"]')
            for t in t0:
                title = t.text
                if title == '': continue
                link = t.get_attribute("href")
                task_map[link] = {"title":title,'cover':''}

            t1 = self.wb.find_elements(By.CSS_SELECTOR,'div[data-testid="Topic"] li')
            for t in t1:
                titleDOM = t.find_element(By.CSS_SELECTOR,'h3[data-testid="Heading"] a')
                title = titleDOM.text
                if title == '': continue
                coverDOM = t.find_element(By.CSS_SELECTOR, 'div[data-testid="Image"]')
                coverHMTL = coverDOM.get_attribute('innerHTML')
                match = re.search(r'src="([^"]*)"', coverHMTL)
                cover = ''
                if match:
                    cover = match.group(1)
                link = titleDOM.get_attribute("href")
                task_map[link] = {"title": title, 'cover': cover}

            print(task_map)

        except BaseException as e:
            print(e)
        GB['bot'].return_pool(self.wb)

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