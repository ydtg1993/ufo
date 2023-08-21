import hashlib
import os
import time

import requests


class ImageDownloader:
    def __init__(self, save_directory, headers=dict, cookies=dict):
        self.save_root = "./resources/"
        self.save_directory = save_directory
        self.max_retries = 12
        self.headers = headers
        self.cookies = cookies
        os.makedirs(self.save_root + self.save_directory, exist_ok=True)

    def download_image(self, url,rename=""):
        relative_path = ""

        for retry in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=10)
                if response.status_code == 200:
                    # 构建图片保存的相对路径
                    _, file_extension = os.path.splitext(url)
                    image_filename = hashlib.md5(url.encode('utf-8')).hexdigest() + file_extension.lower()
                    if rename != "":
                        image_filename = rename + file_extension.lower()
                    relative_path = os.path.join(self.save_directory, image_filename)

                    # 保存图片到指定目录
                    with open(self.save_root + relative_path, "wb") as f:
                        f.write(response.content)
                    break
                else:
                    time.sleep(1)
            except Exception as e:
                print(f"Error while downloading image: {e}. Retrying...")

        return relative_path.replace('\\', '/')