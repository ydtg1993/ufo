import hashlib
import json
import os
import time
from datetime import datetime
import ffmpeg
import m3u8
from selenium.webdriver.common.by import By
import re
from assiatant import GB
from model.new_model import NewModel
from sqlalchemy.exc import OperationalError

class Reuter:
    def __init__(self):
        self.db = GB.mysql
        self.config = GB.config
        self.rd = GB.redis

        try:
            self.wb = GB.bot.start()
            self.url = "https://www.reuters.com"
            self.wb.get(self.url)
            self.login()
            self.wb.get(self.url)
            self.wb.execute_script('''
            window.scrollTo({top: 10000000,behavior: 'smooth'});
                ''')
            time.sleep(2)
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H")
            print("路透社开始任务------------" + formatted_time)
            task_map = {}
            t = self.wb.find_element(By.CSS_SELECTOR, 'ul.home-page-grid__home-hero__N90H7 a[data-testid="Heading"]')
            if t.text != '':
                link = t.get_attribute("href")
                task_map[link] = {"title": t.text, 'cover': ''}

            t0 = self.wb.find_elements(By.CSS_SELECTOR, 'ul.home-page-grid__left-col__2K7_S a[data-testid="Heading"]')
            for t in t0:
                title = t.text
                if title == '': continue
                link = t.get_attribute("href")
                task_map[link] = {"title": title, 'cover': ''}

            t1 = self.wb.find_elements(By.CSS_SELECTOR, 'div[data-testid="Topic"] li')
            for t in t1:
                title_dom = t.find_element(By.CSS_SELECTOR, 'h3[data-testid="Heading"] a')
                title = title_dom.text
                if title == '': continue
                cover_html = t.get_attribute('innerHTML')
                match = re.search(r'src="([^"]*)"', cover_html)
                cover = ''
                if match:
                    cover = match.group(1)
                link = title_dom.get_attribute("href")
                task_map[link] = {"title": title, 'cover': cover}

            box = self.wb.find_element(By.CSS_SELECTOR, 'div.section-selector-tabs__selector-tab-wrapper__2WxjR')
            tabs = box.find_elements(By.CSS_SELECTOR, 'div:first-child div[role="tab"]')
            for tab in tabs:
                tab_id = tab.get_attribute('id')
                self.wb.execute_script(f'document.getElementById("{tab_id}").click();')
                time.sleep(2)
                t2 = box.find_elements(By.CSS_SELECTOR, 'div[role="tabpanel"] li')
                for t in t2:
                    title_dom = t.find_element(By.CSS_SELECTOR, 'a[data-testid="Heading"]')
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

            self.wb.quit()
        except BaseException as e:
            print(e)

    def login(self):
        # cookies = self.rd.get_cache("reuter:cookies")
        # if not cookies :
        self.wb.get(f"{self.url}/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2F")
        time.sleep(3)
        self.wb.find_element(By.CSS_SELECTOR, 'input#email').send_keys("ydtg19930330@gmail.com")
        time.sleep(1)
        self.wb.find_element(By.CSS_SELECTOR, 'input#password').send_keys("Susanoo&87350100")
        time.sleep(1)
        self.wb.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)

    #    cookies = self.wb.get_cookies()
    #    self.rd.set_cache("reuter:cookies",json.dumps(cookies))
    # else:
    #    for cookie in json.loads(cookies):
    #        self.wb.add_cookie(cookie)
    #    self.wb.refresh()

    def run_task(self, task_map):
        for link, task in task_map.items():
            self.wb.get(link)
            time.sleep(3)
            try:
                main = self.wb.find_element(By.ID, 'main-content')
                match = re.match(r'.*<h1 data-testid="Heading".*', main.get_attribute('innerHTML'))
                if not match:
                    continue

                exist = self.db.session.query(NewModel.media_id).filter(NewModel.source_url == link).first()
                if exist is None:
                    cover = task['cover']
                    tags = main.find_elements(By.CSS_SELECTOR, 'nav[aria-label="Tags"] li')
                    categories = []
                    for tag in tags:
                        categories.append(tag.text)

                    full_title = main.find_element(By.CSS_SELECTOR, 'h1[data-testid="Heading"]').text
                    date_str = main.find_element(By.CSS_SELECTOR, 'time span:first-child').text
                    parsed_date = datetime.strptime(date_str, "%B %d, %Y")
                    formatted_date = parsed_date.strftime("%Y-%m-%d")

                    introduce = []
                    content_dom = main.find_element(By.CSS_SELECTOR, 'div.article-body__container__3ypuX')
                    testid = content_dom.find_element(By.CSS_SELECTOR, 'div:first-child').get_attribute('data-testid')
                    if testid == 'primary-image' or testid == 'primary-gallery':
                        img_dom = content_dom.find_element(By.CSS_SELECTOR, 'div:first-child img')
                        cover = img_dom.get_attribute('src')
                        alt = img_dom.get_attribute('alt')
                        introduce.append({'type': 'img', 'val': cover, 'alt': alt})
                    elif testid == 'primary-video':
                        script = self.wb.find_element(By.CSS_SELECTOR,
                                                      'head > script[type="application/ld+json"]').get_attribute(
                            'innerHTML')
                        match = re.search(r'https://[^"]+master\.m3u8', script)
                        if match:
                            md5_hash = hashlib.md5()
                            md5_hash.update(link.encode('utf-8'))
                            playlist = m3u8.load(match.group(), 30, {
                                "Referer": "https://www.reuters.com",
                                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                            })
                            uri = playlist.data.get('playlists')[5]['uri']
                            today = datetime.today()
                            path = f"vd/{today.strftime('%m')}"
                            file = f"{md5_hash.hexdigest()}.mp4"
                            print(uri)
                            os.makedirs("./" + path, exist_ok=True)
                            for i in range(6):
                                try:
                                    ffmpeg.input(uri).output(f"./{path}/{file}").run(capture_stdout=True,
                                                                                     capture_stderr=True)
                                    introduce.append({'type': 'video', 'val': f"{path}/{file}", 'm3u8': uri})
                                    break
                                except ffmpeg.Error as e:
                                    if i == 4:
                                        uri = playlist.data.get('playlists')[4]['uri']
                                    if i == 5:
                                        print("FFmpeg error:" + e.stderr.decode('utf-8'))

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

                    NewModel(title=task['title'],
                             cover=cover,
                             full_title=full_title,
                             source_url=link,
                             introduce=json.dumps(introduce),
                             source_id=6,
                             categories=json.dumps(categories),
                             publish_at=formatted_date).insert()
            except OperationalError as e:
                print(e)
                GB.mysql.reconnect()
            except Exception as e:
                print(e, link)
                continue