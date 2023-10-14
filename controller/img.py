import json
import math
import re
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from assiatant import GB
from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel
from PIL import Image
import requests
from io import BytesIO


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
            vh = wb.execute_script('return document.body.scrollHeight')
            h = 5000
            second = math.ceil(vh / h)
            wb.execute_script('''
let f1 = setInterval(()=>{
 let dom = document.documentElement;
 const currentScroll = dom.scrollTop 
 const clientHeight = dom.clientHeight; 
 const scrollHeight = dom.scrollHeight; 
 if (scrollHeight+10 > currentScroll + clientHeight) {
     dom.scrollTo({'left':0,'top': currentScroll + 5000,behavior: 'smooth'})
  }else{
     clearInterval(f1);			
  }
},500);
            ''')
            time.sleep(second)

            divs = wb.find_elements(By.CSS_SELECTOR, '.comic-contain div')
            img_list = []
            for _, div in enumerate(divs):
                try:
                    html = div.get_attribute('innerHTML')
                    if not re.match(r'.*<amp-img.*', html):
                        continue
                    src = div.find_element(By.TAG_NAME, 'amp-img').get_attribute('data-src')
                    response = requests.get(src, {
                        "Referer": url,
                    })
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        width, height = image.size
                        img_list.append({'s': src, 'w': width, 'h': height})
                except StaleElementReferenceException:
                    pass

            if len(img_list) > 0:
                try:
                    record.images = json.dumps(img_list)
                    record.img_count = len(img_list)
                    count = GB.mysql.session.query(SourceChapterModel).filter(
                        SourceChapterModel.comic_id == record.comic_id).count()
                    GB.mysql.session.query(SourceComicModel).filter(SourceComicModel.id == record.comic_id).update(
                        {SourceComicModel.chapter_count: count,
                         SourceComicModel.last_chapter_update_at: record.created_at})
                    GB.mysql.session.commit()
                except Exception:
                    GB.mysql.session.rollback()
                    GB.mysql.reconnect()

        wb.quit()
