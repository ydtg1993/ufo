import json
import logging
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from sqlalchemy.exc import OperationalError
from assiatant import GB
from model.new_model import NewModel
import re


class Nytime:
    session = None

    def __init__(self):
        self.session = GB.mysql.connect()
        self.url = "https://cn.nytimes.com"
        self.wb = GB.bot.retry_start(self.url)

        try:
            self.wb.execute_script('''
            window.scrollTo({top: 10000000,behavior: 'smooth'});
                ''')
            time.sleep(7)
            task_map = {}

            t0 = self.wb.find_elements(By.CSS_SELECTOR, "h3.regularSummaryHeadline")
            self.fill_task(task_map, t0)

            t1 = self.wb.find_elements(By.CSS_SELECTOR, "ol.hotStoryList>li")
            self.fill_task(task_map, t1)

            t2 = self.wb.find_elements(By.CSS_SELECTOR, "ul.headlineOnlyList h3")
            self.fill_task(task_map, t2)

            t3 = self.wb.find_elements(By.CSS_SELECTOR, "#moth .cf h3")
            self.fill_task(task_map, t3)

            t4 = self.wb.find_elements(By.CSS_SELECTOR, "#well h3")
            self.fill_task(task_map, t4)

            self.run_task(task_map)
            self.wb.quit()
        except BaseException as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            self.wb.quit()
            self.session.close()

    @staticmethod
    def fill_task(task_map, doms):
        for t in doms:
            a = t.find_element(By.TAG_NAME, 'a')
            title = a.get_attribute("title")
            if title == '':
                continue
            link = a.get_attribute("href")
            task_map[title] = link

    def run_task(self, task_map):
        for title, link in task_map.items():
            self.wb.get(link)
            time.sleep(3)
            try:
                body = self.wb.find_element(By.TAG_NAME, 'body')
                match = re.match(r'.*class="article-area".*', body.get_attribute('innerHTML'))
                if not match:
                    continue

                area = self.wb.find_element(By.CLASS_NAME, 'article-area')
                exist = self.session.query(NewModel.media_id).filter(NewModel.title == title).first()
                if exist is None:
                    categories = []
                    category = area.find_element(By.CSS_SELECTOR, ".setting-bar>.section-title>h3").text
                    categories.append(category)
                    publish_at = area.find_element(By.CSS_SELECTOR, "div.article-header time").get_attribute('datetime')

                    introduce = []
                    banner = area.find_element(By.CSS_SELECTOR, "figure.article-span-photo img")
                    cover = banner.get_attribute('src')
                    alt = banner.get_attribute('alt')
                    introduce.append({'type': 'img', 'val': cover, 'alt': alt})

                    paragraph = self.wb.find_elements(By.CLASS_NAME, "article-paragraph")
                    for p in paragraph:
                        childrenDom = p.get_attribute('innerHTML')
                        if re.compile(r'<b>.*?</b>').search(childrenDom):
                            introduce.append({'type': 'b', 'val': p.text})
                        elif re.compile(r'<img').search(childrenDom):
                            imgDom = p.find_element(By.TAG_NAME, 'img')
                            cover = imgDom.get_attribute('data-src')
                            alt = imgDom.get_attribute('alt')
                            introduce.append({'type': 'img', 'val': cover, 'alt': alt})
                        else:
                            introduce.append({'type': 'text', 'val': p.text})

                    news = NewModel(title=title,
                                    cover=cover,
                                    full_title=area.find_element(By.CSS_SELECTOR, '.article-header h1').text,
                                    source_url=link,
                                    introduce=json.dumps(introduce),
                                    source_id=8,
                                    categories=json.dumps(categories),
                                    publish_at=publish_at)
                    self.session.add(news)
                    self.session.commit()
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))
