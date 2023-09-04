import time
from selenium.webdriver.common.by import By
from assiatant.downloader import ImageDownloader
from assiatant.globe import GB
from model.cate_model import CateModel
from model.new_model import NewModel
import re


class Nytime:
    def __init__(self):
        self.db = GB['mysql']
        self.config = GB['config']
        self.wb = GB['bot'].start()
        self.url = "https://cn.nytimes.com"

        self.wb.get(self.url)
        self.wb.execute_script('''
        window.scrollTo({top: 10000000,behavior: 'smooth'});
            ''')
        time.sleep(2)
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

        self.wb.close()

    @staticmethod
    def fill_task(task_map,doms):
        for t in doms:
            a = t.find_element(By.TAG_NAME, 'a')
            title = a.get_attribute("title")
            if title == '' :continue
            link = a.get_attribute("href")
            task_map[title] = link


    def run_task(self,task_map):
        for title, link in task_map.items():
            self.wb.get(link)
            time.sleep(3)
            try:
                main = self.wb.find_element(By.CLASS_NAME, 'article-area')
                exist = self.db.session.query(NewModel.media_id).filter(NewModel.title == title).first()
                if exist is None:
                    category = main.find_element(By.CSS_SELECTOR,".setting-bar>.section-title>h3").text
                    categoryId = CateModel.get_or_create_id_by_name(self.db.session,category)

                    introduce = ""
                    banner = main.find_element(By.CSS_SELECTOR, "figure.article-span-photo img")
                    cover = banner.get_attribute('src')
                    alt = banner.get_attribute('alt')
                    introduce += f"![{alt}]({cover} \"{alt}\")  "

                    paragraph = self.wb.find_elements(By.CLASS_NAME, "article-paragraph")
                    for p in paragraph:
                        childrenDom = p.get_attribute('innerHTML')
                        if re.compile(r'<b>.*?</b>').search(childrenDom):
                            introduce += f"## {p.text}  "
                        elif re.compile(r'<img').search(childrenDom):
                            imgDom = p.find_element(By.TAG_NAME, 'img')
                            cover = imgDom.get_attribute('data-src')
                            alt = imgDom.get_attribute('alt')
                            introduce += f"![{alt}]({cover} \"{alt}\")  "
                        else:
                            introduce += f"\n{p.text}\n"

                    new = NewModel(title=title,
                                   cover=cover,
                                   full_title=main.find_element(By.CSS_SELECTOR, '.article-header h1').text,
                                   source_url=link,
                                   introduce=introduce,
                                   source_id=8,
                                   category_id=categoryId, )
                    self.db.session.add(new)
                    self.db.session.commit()
            except Exception as e:
                print(e)
                continue


