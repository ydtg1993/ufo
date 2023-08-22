import time
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from assiatant.bot import Bot
from assiatant.db import MysqlConnector
from assiatant.downloader import ImageDownloader
from assiatant.proxy import Proxy
from assiatant.rd import RedisConnector
from configparser import ConfigParser
from model.new_model import NewModel
import re
import json

class Volume:
    def __init__(self, **kwargs):
        CONF: ConfigParser = kwargs.get('CONF')
        DB: MysqlConnector = kwargs.get('DB_POOL')
        RD: RedisConnector = kwargs.get('RD_POOL')
        BOT: Bot = kwargs.get('BOT')
        WB: Chrome = BOT.start()
        url = CONF.get("App", "SOURCE_URL")

        WB.get(f"{url}")

        task_map = {}

        t0 = WB.find_elements(By.CSS_SELECTOR,"h3.regularSummaryHeadline")
        for t in t0 :
            a = t.find_element(By.TAG_NAME,'a')
            title = a.get_attribute("title")
            link = a.get_attribute("href")
            task_map[title] = link

        t1 = WB.find_elements(By.CSS_SELECTOR,"ol.hotStoryList>li")
        for t in t1:
            a = t.find_element(By.TAG_NAME, 'a')
            title = a.get_attribute("title")
            link = a.get_attribute("href")
            task_map[title] = link

        for title, link in task_map.items():
            WB.get(link)
            time.sleep(3)
            try:
                main = WB.find_element(By.CLASS_NAME,'article-area')
                exist = DB.session.query(NewModel).filter(NewModel.source_url==link).first()
                if exist is None:
                    desc = []
                    banner = main.find_element(By.CSS_SELECTOR,"figure.article-span-photo img")
                    desc.append({'type':'img','val':banner.get_attribute('src'),'alt':banner.get_attribute('alt')})
                    paragraph = WB.find_elements(By.CLASS_NAME,"article-paragraph")
                    for p in paragraph:
                        childrenDom = p.get_attribute('innerHTML')
                        if re.compile(r'<b>.*?</b>').search(childrenDom):
                            desc.append({'type':'b','val':p.text})
                        elif re.compile(r'<img').search(childrenDom):
                            imgDom = p.find_element(By.TAG_NAME,'img')
                            desc.append({'type': 'img', 'val': imgDom.get_attribute('data-src'),'alt':imgDom.get_attribute('alt')})
                        else :
                            desc.append({'type':'text','val':p.text})

                    new = NewModel(title=title,
                             full_title=main.find_element(By.CSS_SELECTOR,'.article-header h1').text,
                             source_url=link,
                             introduce=json.dumps(desc),
                             source_id=8,
                             category_id=1,)
                    DB.session.add(new)
                    DB.session.commit()
            except Exception as e:
                print(e)
                continue

        WB.close()