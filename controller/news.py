import time
from selenium.webdriver.common.by import By
from assiatant.downloader import ImageDownloader
from assiatant.globe import GB
from model.new_model import NewModel
import re
import json


class News:
    def __init__(self):
        db = GB['mysql']
        config = GB['config']
        wb = GB['bot'].start()
        url = config.get("App", "SOURCE_URL")

        wb.get(url)

        task_map = {}
        t0 = wb.find_elements(By.CSS_SELECTOR, "h3.regularSummaryHeadline")
        for t in t0:
            a = t.find_element(By.TAG_NAME, 'a')
            title = a.get_attribute("title")
            link = a.get_attribute("href")
            task_map[title] = link

        t1 = wb.find_elements(By.CSS_SELECTOR, "ol.hotStoryList>li")
        for t in t1:
            a = t.find_element(By.TAG_NAME, 'a')
            title = a.get_attribute("title")
            link = a.get_attribute("href")
            task_map[title] = link

        for title, link in task_map.items():
            wb.get(link)
            time.sleep(3)
            try:
                main = wb.find_element(By.CLASS_NAME, 'article-area')
                exist = db.session.query(NewModel).filter(NewModel.title == title).first()
                if exist is None:
                    desc = []
                    banner = main.find_element(By.CSS_SELECTOR, "figure.article-span-photo img")
                    cover = banner.get_attribute('src')
                    desc.append({'type': 'img', 'val': cover, 'alt': banner.get_attribute('alt')})
                    paragraph = wb.find_elements(By.CLASS_NAME, "article-paragraph")
                    for p in paragraph:
                        childrenDom = p.get_attribute('innerHTML')
                        if re.compile(r'<b>.*?</b>').search(childrenDom):
                            desc.append({'type': 'b', 'val': p.text})
                        elif re.compile(r'<img').search(childrenDom):
                            imgDom = p.find_element(By.TAG_NAME, 'img')
                            desc.append({'type': 'img', 'val': imgDom.get_attribute('data-src'),
                                         'alt': imgDom.get_attribute('alt')})
                        else:
                            desc.append({'type': 'text', 'val': p.text})

                    new = NewModel(title=title,
                                   cover=cover,
                                   full_title=main.find_element(By.CSS_SELECTOR, '.article-header h1').text,
                                   source_url=link,
                                   content=json.dumps(desc),
                                   introduce=self.j2m(json.dumps(desc)),
                                   source_id=8,
                                   category_id=1, )
                    db.session.add(new)
                    db.session.commit()
            except Exception as e:
                print(e)
                continue

        wb.close()

    def j2m(self,data, level=0):
        if isinstance(data, dict):
            markdown = ""
            for key, value in data.items():
                markdown += "  " * level + f"- **{key}**:\n" + self.j2m(value, level + 1)
        elif isinstance(data, list):
            markdown = ""
            for item in data:
                markdown += "  " * level + "- " + self.j2m(item, level + 1)
        else:
            markdown = str(data) + "\n"

        return markdown
