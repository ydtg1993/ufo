import re
import time
from selenium.webdriver.common.by import By
from assiatant import GB
import json
from model.source_comic_model import SourceComicModel


class Chapter:
    def __init__(self):
        wb = GB.bot.start()
        wb.get(GB.config.get("App", "URL"))
        time.sleep(3)
        for _ in range(12):
            comic_id = GB.redis.dequeue(GB.config.get("Redis", "PREFIX") + "chapter:task")
            if comic_id is None:
                return

            record = GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.id == comic_id).first()
            if record is None:
                return
            wb.get(record.source_url)
            time.sleep(3)

            chapter_dom = wb.find_element(By.CSS_SELECTOR, "div.comics-detail > div:nth-child(3)")
            match = re.match(r'.*id="chapter-items".*', chapter_dom.get_attribute('innerHTML'))
            if match:
                chapter_doms = chapter_dom.find_elements(By.CSS_SELECTOR, "#chapter-items a")

        wb.quit()
