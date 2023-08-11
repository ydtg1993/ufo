import undetected_chromedriver as uc
import threading
import time

def thread_function():
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, user_multi_procs=True)
    time.sleep(7)
    driver.get('https://www.manhuagui.com/')


threads = []
for i in range(2):
    thread = threading.Thread(target=thread_function, args=())
    threads.append(thread)
    thread.start()

# 等待所有线程结束
for thread in threads:
    thread.join()

input("按任意键退出...")