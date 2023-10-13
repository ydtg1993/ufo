import re
import time
from selenium.webdriver.common.by import By
from assiatant import GB

from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel


class Img:
    def __init__(self):
        wb = GB.bot.start()
        url = GB.config.get("App", "URL")
        wb.get(url)
        time.sleep(3)
        for _ in range(12):
            chapter_id = GB.redis.dequeue(GB.config.get("App", "PROJECT") + ":img:task")
            if chapter_id is None:
                return

            record = GB.mysql.session.query(SourceChapterModel).filter(SourceComicModel.id == chapter_id).first()
            if record is None:
                break
            wb.get(record.source_url)
            time.sleep(3)

            chapter_dom = wb.find_element(By.CSS_SELECTOR, "div.comics-detail > div:nth-child(3)")
            if not re.match(r'.*class="pure-g".*', chapter_dom.get_attribute('innerHTML')):
                continue

        wb.quit()
