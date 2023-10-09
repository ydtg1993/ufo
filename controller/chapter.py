import time

from selenium.webdriver.common.by import By

from assiatant import GB
import json

from model.source_comic_model import SourceComicModel


class Chapter:
    def __init__(self):
        wb = GB.bot.start()
        for _ in range(12):
            wb.get(GB.config.get("App", "URL"))
            time.sleep(3)

            comic_id = GB.redis.dequeue(GB.config.get("Redis", "PREFIX") + "chapter:task")
            if comic_id is None:
                return

            record = GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.id == comic_id).first()
            if record is None:
                return
            wb.get(record.source_url)

        wb.quit()
