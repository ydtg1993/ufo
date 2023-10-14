import re
import time
from selenium.webdriver.common.by import By
from assiatant import GB

from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel


class Chapter:
    def __init__(self):
        wb = GB.bot.start()
        url = GB.config.get("App", "URL")
        wb.get(url)
        time.sleep(3)
        for _ in range(12):
            comic_id = GB.redis.dequeue(GB.config.get("App", "PROJECT") + ":chapter:task")
            if comic_id is None:
                return

            record = GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.id == comic_id).first()
            if record is None:
                break
            wb.get(record.source_url)
            time.sleep(3)

            chapter_dom = wb.find_element(By.CSS_SELECTOR, "div.comics-detail > div:nth-child(3)")
            if not re.match(r'.*class="pure-g".*', chapter_dom.get_attribute('innerHTML')):
                continue

            if re.match(r'.*id="chapter-items".*', chapter_dom.get_attribute('innerHTML')):
                chapters = chapter_dom.find_elements(By.CSS_SELECTOR, "#chapter-items a")
                chapters.extend(chapter_dom.find_elements(By.CSS_SELECTOR, "#chapters_other_list a"))
                self.chapter_patch(comic_id, chapters)
            else:
                chapters = chapter_dom.find_elements(By.CSS_SELECTOR, ".pure-g a")
                chapters.reverse()
                self.chapter_patch(comic_id, chapters)
        wb.quit()

    def chapter_patch(self, comic_id, chapters):
        for sort, chapter in enumerate(chapters):
            link = chapter.get_attribute('href')
            title = chapter.get_attribute('textContent')
            if GB.redis.get_hash(GB.config.get("App", "PROJECT") + ":unique:chapter:link", link) is not None:
                continue

            i = SourceChapterModel(title=title,
                                   comic_id=comic_id,
                                   source_url=link,
                                   images='[]',
                                   sort=sort).insert()
            GB.redis.set_hash(GB.config.get("App", "PROJECT") + ":unique:chapter:link", link, "0")
            GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":img:task", i)
