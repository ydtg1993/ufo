import hashlib
import json
import random
import time
from datetime import datetime
from selenium.webdriver.common.by import By

from assiatant.downloader import M3u8Downloader
from assiatant.globe import GB
import re
from model.new_model import NewModel


class Reuter:
    def __init__(self):
        self.db = GB['mysql']
        self.config = GB['config']
        self.rd = GB["redis"]
        self.wb = GB['bot'].get_pool()
        self.url = "https://www.reuters.com"
        self.run_task({"https://www.reuters.com/business/autos-transportation/us-auto-union-strike-three-detroit-three-factories-2023-09-15/":{"title": '22', 'cover': '22'}})
        time.sleep(30000000)
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
                title_dom = t.find_element(By.CSS_SELECTOR,'h3[data-testid="Heading"] a')
                title = title_dom.text
                if title == '': continue
                cover_html = t.get_attribute('innerHTML')
                match = re.search(r'src="([^"]*)"', cover_html)
                cover = ''
                if match:
                    cover = match.group(1)
                link = title_dom.get_attribute("href")
                task_map[link] = {"title": title, 'cover': cover}

            box = self.wb.find_element(By.CSS_SELECTOR,'div.section-selector-tabs__selector-tab-wrapper__2WxjR')
            tabs = box.find_elements(By.CSS_SELECTOR,'div:first-child div[role="tab"]')
            for tab in tabs:
                tab_id = tab.get_attribute('id')
                self.wb.execute_script(f'document.getElementById("{tab_id}").click();')
                time.sleep(2)
                t2 = box.find_elements(By.CSS_SELECTOR,'div[role="tabpanel"] li')
                for t in t2:
                    title_dom = t.find_element(By.CSS_SELECTOR,'a[data-testid="Heading"]')
                    title = title_dom.text
                    if title == '': continue
                    cover_html = t.get_attribute('innerHTML')
                    match = re.search(r'src="([^"]*)"', cover_html)
                    cover = ''
                    if match:
                        cover = match.group(1)
                    link = title_dom.get_attribute("href")
                    task_map[link] = {"title": title, 'cover': cover}

            self.run_task(task_map)

        except BaseException as e:
            print(e)
        GB['bot'].return_pool(self.wb)

    def login(self):
        btn = self.wb.find_element(By.CLASS_NAME,"site-header__button-group__5IlZj")
        btn_html = btn.get_attribute("innerHTML")
        if re.compile(r'hk').search(btn_html):
            return

        self.wb.get(f"{self.url}/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2F")
        time.sleep(3)
        self.wb.find_element(By.CSS_SELECTOR, 'input#email').send_keys("ydtg19930330@gmail.com")
        time.sleep(1)
        self.wb.find_element(By.CSS_SELECTOR, 'input#password').send_keys("Susanoo&87350100")
        time.sleep(1)
        self.wb.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)

    def run_task(self, task_map):
        for link,task in task_map.items():
            self.wb.get(link)
            time.sleep(3)
            try:
                main = self.wb.find_element(By.ID,'main-content')
                match = re.match(r'.*data-testid="Heading".*', main.get_attribute('innerHTML'))
                if not match:
                    continue

                exist = self.db.session.query(NewModel.media_id).filter(NewModel.source_url == link).first()
                if exist is None:
                    cover = task['cover']
                    tags = main.find_elements(By.CSS_SELECTOR,'nav[aria-label="Tags"] li')
                    categories = []
                    for tag in tags:
                        categories.append(tag.text)

                    full_title = main.find_element(By.CSS_SELECTOR,'h1[data-testid="Heading"]').text
                    date_str = main.find_element(By.CSS_SELECTOR,'time[data-testid="Text"] span:first-child').text
                    parsed_date = datetime.strptime(date_str, "%B %d, %Y")
                    formatted_date = parsed_date.strftime("%Y-%m-%d")

                    introduce = []
                    content_dom = main.find_element(By.CSS_SELECTOR,'div.article-body__container__3ypuX')
                    testid = content_dom.find_element(By.CSS_SELECTOR, 'div:first-child').get_attribute('data-testid')
                    if testid == 'Image':
                        img_dom = content_dom.find_element(By.CSS_SELECTOR, 'div:first-child img')
                        cover = img_dom.get_attribute('src')
                        alt = img_dom.get_attribute('alt')
                        introduce.append({'type': 'img', 'val': cover, 'alt': alt})
                    elif testid == 'primary-video':
                        script = self.wb.find_element(By.CSS_SELECTOR,'head > script[type="application/ld+json"]').get_attribute('innerHTML')
                        match = re.search(r'https://[^"]+master\.m3u8', script)
                        # 打印匹配结果
                        if match:
                            m3u8 = match.group()
                            cookies = self.wb.get_cookies()
                            combined_cookies = {}
                            for cookie in cookies:
                                combined_cookies[cookie["name"]] = cookie["value"]

                            md5_hash = hashlib.md5()
                            md5_hash.update(link.encode('utf-8'))
                            img_downLoader = M3u8Downloader(str(random.randint(0, 256)), {
                                "Referer": "https://www.reuters.com",
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                            }, combined_cookies).download_image(m3u8,md5_hash.hexdigest())


                    paragraph = content_dom.find_elements(By.CSS_SELECTOR, 'div:nth-child(2) p,div:nth-child(2) figure')
                    for p in paragraph:
                        if p.tag_name == 'figure':
                            match = re.match(r'src="([^"]*)"', p.get_attribute('innerHTML'))
                            if match:
                                img_dom = p.find_element(By.TAG_NAME, 'img')
                                cover = img_dom.get_attribute('src')
                                alt = img_dom.get_attribute('alt')
                                introduce.append({'type': 'img', 'val': cover, 'alt': alt})
                        else:
                            introduce.append({'type': 'text', 'val': p.text})

                    new = NewModel(title=task['title'],
                                   cover=cover,
                                   full_title=full_title,
                                   source_url=link,
                                   introduce=json.dumps(introduce),
                                   source_id=6,
                                   categories=json.dumps(categories),
                                   publish_at=formatted_date)
                    self.db.session.add(new)
                    self.db.session.commit()
            except Exception as e:
                print(e)
                continue