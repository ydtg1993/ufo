import logging
import random
import re
import time
from selenium.webdriver.common.by import By
from assiatant import GB
import json
from director.info import Info
from model.source_video_model import SourceVideoModel


class Detail:
    session = None

    def __init__(self):
        self.session = GB.mysql.connect()
        wb = GB.bot.retry_start(GB.config.get("App", "URL"))
        try:
            self.insert_process(wb)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            wb.quit()
            self.session.close()

    def insert_process(self, wb):
        for _ in range(12):
            i = Info()
            i.check_stop_signal()
            try:
                task = GB.redis.dequeue(GB.process_cache_conf['detail']['key'])
                if task is None:
                    time.sleep(random.randint(900, 1200))
                    break
                task = json.loads(task)
                time.sleep(random.randint(7, 30))
                title = task['title']
                link = task['link']
                i.insert_current_task('img', f'详情导入《{title}》-{link}')
                exist = self.session.query(SourceVideoModel).filter(
                    SourceVideoModel.source_url == task['link']).first()
                if exist is not None:
                    continue
                wb.get(task['link'])
                if not re.match(r'.*class="MacPlayer".*',
                                wb.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML'),
                                re.DOTALL):
                    continue

                detail_id = self.comic_info(wb, task)
                if detail_id:
                    receiver = {'video':'','cover':''}
                    self.sync_receive_info(receiver,
                                           video=GB.process_cache_conf['hook_video']['key'],
                                           cover=GB.process_cache_conf['hook_cover']['key'])
                    GB.redis.delete(GB.process_cache_conf['hook_video']['key'])
                    GB.redis.delete(GB.process_cache_conf['hook_cover']['key'])
                    self.session.query(SourceVideoModel).filter(SourceVideoModel.id == detail_id).update({
                        SourceVideoModel.url: receiver['video'],
                        SourceVideoModel.big_cover: receiver['cover']})
                    self.session.commit()
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.exception(str(e))

    def sync_receive_info(self,receiver, **kwargs):
        for _ in range(15):
            time.sleep(1)
            for key, value in kwargs.items():
                cache = GB.redis.get_cache(value)
                if cache is not None and cache != '' and receiver[key] == '':
                    receiver[key] = cache
            for _,value in receiver.items():
                if value == '':
                    break
            else:
                break

    def comic_info(self, wb, task):
        exist = self.session.query(SourceVideoModel).filter(SourceVideoModel.source_url == task['link']).first()
        if exist is not None:
            return
        info_dom = wb.find_element(By.CSS_SELECTOR, "div.detail")
        dds = info_dom.find_elements(By.TAG_NAME, 'dd')
        number = dds[1].text
        producer = dds[3].text
        publish_time = dds[5].text
        description = wb.find_element(By.CSS_SELECTOR, '.des_xy').text
        actors = []
        for _, a in enumerate(dds[0].find_elements(By.TAG_NAME, 'a')):
            if a.text == '未知' or a.text == '':
                continue
            actors.append(a.text)
        tags = []
        for _, a in enumerate(dds[2].find_elements(By.TAG_NAME, 'a')):
            if a.text == '':
                continue
            tags.append(a.text)
        detail = SourceVideoModel(title=task['title'],
                                  source_url=task['link'],
                                  cover=task['cover'],
                                  number=number,
                                  producer=producer,
                                  actors=json.dumps(actors),
                                  label=json.dumps(tags),
                                  publish_time=publish_time,
                                  description=description)
        self.session.add(detail)
        self.session.commit()
        return detail.id
