import os
import time

import requests


class ImageDownloader:
    def __init__(self, save_directory, rename="", headers=None, cookies=None):
        self.save_directory = save_directory
        self.max_retries = 12
        self.rename = rename
        self.headers = headers
        self.cookies = cookies
        os.makedirs(self.save_directory, exist_ok=True)

    def download_image(self, url):
        relative_path = None

        for retry in range(self.max_retries):
            try:
                response = requests.get(url, headers=self.headers, cookies=self.cookies)
                if response.status_code == 200:
                    # 构建图片保存的相对路径
                    image_filename = url.split("/")[-1]
                    if self.rename != "":
                        image_filename = self.rename
                    relative_path = os.path.join(self.save_directory, image_filename)

                    # 保存图片到指定目录
                    with open(relative_path, "wb") as f:
                        f.write(response.content)

                    print("Image downloaded successfully:", relative_path)
                    break
                else:
                    print("Failed to download image. Retrying...")
                    time.sleep(1)
            except Exception as e:
                print(f"Error while downloading image: {e}. Retrying...")

        return relative_path