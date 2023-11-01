import json
import logging
import math
import random
import re
import time
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from assiatant import GB
from director.info import Info
from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel
from PIL import Image
import requests
from io import BytesIO


class Img:
    def __init__(self):
        wb = GB.bot.retry_start(GB.config.get("App", "URL"))
        session = GB.mysql.connect()
        for _ in range(20):
            i = Info()
            i.check_stop_signal()
            try:
                chapter_id = GB.redis.dequeue(GB.process_cache_conf['img']['key'])
                if chapter_id is None:
                    time.sleep(random.randint(300, 600))
                    break

                record = session.query(SourceChapterModel).filter(
                    SourceChapterModel.id == chapter_id).first()
                if record is None:
                    continue
                i.insert_current_task('img', f'章节{record.title} - {chapter_id}图片处理')
                wb.get(record.source_url)
                vh = wb.execute_script('return document.body.scrollHeight')
                h = 1800
                second = math.ceil(vh / h)
                wb.execute_script('''
    let f1 = setInterval(()=>{
     let dom = document.documentElement;
     const currentScroll = dom.scrollTop 
     const clientHeight = dom.clientHeight; 
     const scrollHeight = dom.scrollHeight; 
     if (scrollHeight+10 > currentScroll + clientHeight) {
         dom.scrollTo({'left':0,'top': currentScroll + 1800,behavior: 'smooth'})
      }else{
         clearInterval(f1);			
      }
    },500);
                ''')

                divs = wb.find_elements(By.CSS_SELECTOR, 'img.img_content_jpg')
                img_list = []
                for _, div in enumerate(divs):
                    try:
                        alt = div.get_attribute('alt')
                        if not re.match(r'.*chapter.*', alt):
                            continue
                        src = div.get_attribute('data-src')
                        #response = requests.get(src, {
                        #    "Referer": url,
                        #})
                        #if response.status_code == 200:
                        #    image = Image.open(BytesIO(response.content))
                        #    width, height = image.size
                        #    img_list.append({'s': src, 'w': width, 'h': height})
                        img_list.append(src)
                    except StaleElementReferenceException:
                        pass

                if len(img_list) > 0:
                    record.images = json.dumps(img_list)
                    record.img_count = len(img_list)
                    count = session.query(SourceChapterModel).filter(
                        SourceChapterModel.comic_id == record.comic_id).count()

                    session.query(SourceComicModel).filter(
                        SourceComicModel.id == record.comic_id).update(
                        {SourceComicModel.chapter_count: count,
                         SourceComicModel.last_chapter_update_at: record.created_at})
                    session.commit()
                time.sleep(second)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))
            finally:
                session.close()
        wb.quit()
