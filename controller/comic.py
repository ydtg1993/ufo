import time
from selenium.webdriver.common.by import By
from assiatant.downloader import ImageDownloader
from assiatant.globe import GB
from model.source_comic_model import SourceComicModel


class Comic:
    def __init__(self, **kwargs):
        db = GB['mysql']
        config = GB['config']
        wb = GB['bot'].start()
        url = config.get("App", "SOURCE_URL")

        wb.get(url + "/allmanga/")

        cookies = wb.get_cookies()
        combined_cookies = {}
        for cookie in cookies:
            combined_cookies[cookie["name"]] = cookie["value"]

        time.sleep(5)
        comic_elems = wb.find_elements(By.CSS_SELECTOR, ".entries>article")
        img_downLoader = ImageDownloader("comic", {
            "Referer": "https://baozimh.org/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }, combined_cookies)
        for comic_elem in comic_elems:
            t_dom = comic_elem.find_element(By.CLASS_NAME, "entry-title")
            title = t_dom.text.strip()
            source_url = t_dom.find_element(By.TAG_NAME, 'a').get_attribute('href')
            exist = db.session.query(SourceComicModel).filter(SourceComicModel.source_url == source_url).first()
            if exist is None:
                cover = comic_elem.find_element(By.TAG_NAME, "img").get_attribute("data-src")
                cover = img_downLoader.download_image(cover)
                comic = SourceComicModel(title=title,
                                         source_url=source_url,
                                         cover=cover,
                                         source_data=comic_elem.get_attribute('innerHTML')
                                         )
                db.session.add(comic)
                db.session.commit()
