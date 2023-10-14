import math
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
        for _ in range(20):
            chapter_id = GB.redis.dequeue(GB.config.get("App", "PROJECT") + ":img:task")
            if chapter_id is None:
                return

            record = GB.mysql.session.query(SourceChapterModel).filter(SourceChapterModel.id == chapter_id).first()
            if record is None:
                break
            wb.get(record.source_url)
            time.sleep(3)
            vh = wb.execute_script('return document.body.scrollHeight')
            h = 5000
            second = math.ceil(vh / h)
            wb.execute_script('''
function smoothScrollDown(distance, duration, currentScroll = 0) {
    const scrollStep = distance / (duration / 1000); // 计算每秒的滚动距离

    if (currentScroll + scrollStep >= distance) {
        // 已经滚动到底部，停止滚动
        window.scrollTo(0, distance);
    } else {
        // 还未滚动到底部，继续滚动
        currentScroll += scrollStep;
        window.scrollTo(0, currentScroll);
        setTimeout(function() {
            smoothScrollDown(distance, duration, currentScroll);
        }, 1000); // 每秒执行一次
    }
}
smoothScrollDown(5000, 1000);
            ''')
            time.sleep(second)

            img = wb.find_element(By.CSS_SELECTOR, '.comic-contain')
            s = img.get_attribute('innerHTML')
            print(s)
        wb.quit()
