import logging
import random
import time
import schedule
from assiatant import GB
from controller.comic import Comic
from controller.img import Img
from controller.menu import Menu
from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel


def main():
    schedule.every(15).minutes.do(process_menu)
    schedule.every(3).minutes.do(process_comic).tag('enabled')
    schedule.every(2).minutes.do(process_img).tag('enabled')
    schedule.every(45).minutes.do(process_update_comic).tag('enabled')
    schedule.every(3).hours.do(reset_comic_update_queue).tag('enabled')
    schedule.every(12).hours.do(reset_chapter_img_queue).tag('enabled')
    while True:
        schedule.run_pending()
        time.sleep(5)


def process_menu():
    while True:
        try:
            Menu()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        time.sleep(random.randint(900, 3600))


def process_comic():
    try:
        Comic()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(str(e))


def process_img():
    try:
        Img()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(str(e))


def process_update_comic():
    try:
        Comic(True)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(str(e))


def reset_comic_update_queue():
    try:
        batch_size = 500
        offset = 0
        tasks = GB.redis.get_queue(GB.config.get("App", "PROJECT") + ":chapter:task", 0, -1)
        while True:
            results = GB.mysql.session.query(SourceComicModel.id).filter(
                SourceComicModel.source_chapter_count != SourceComicModel.chapter_count).offset(offset).limit(
                batch_size).all()
            for result in results:
                tasks.append(str(result[0]))
            tasks = list(set(tasks))
            offset += batch_size
            if len(results) < batch_size:
                GB.redis.delete(GB.config.get("App", "PROJECT") + ":chapter:task")
                for _, comic_id in enumerate(tasks):
                    GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":chapter:task", comic_id)
                break
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(str(e))


def reset_chapter_img_queue():
    try:
        batch_size = 500
        offset = 0
        tasks = GB.redis.get_queue(GB.config.get("App", "PROJECT") + ":img:task", 0, -1)
        while True:
            results = GB.mysql.session.query(SourceChapterModel.id).filter(
                SourceChapterModel.img_count == 0).offset(offset).limit(
                batch_size).all()
            for result in results:
                tasks.append(str(result[0]))
            tasks = list(set(tasks))
            offset += batch_size
            if len(results) < batch_size:
                GB.redis.delete(GB.config.get("App", "PROJECT") + ":img:task")
                for _, chapter_id in enumerate(tasks):
                    GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":img:task", chapter_id)
                break
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(str(e))


if __name__ == '__main__':
    main()
