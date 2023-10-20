import json
import time

from assiatant import GB
from assiatant.singleton import Singleton


@Singleton
class Info(object):
    _stop_task_num = 0
    _stop_signal = False

    def __init__(self):
        self.process_key = GB.config.get("App", "PROJECT") + ':process:board'
        self.stop_task_num_key = GB.config.get("App", "PROJECT") + ':stop:task:num'

    def insert_process(self, name, time, life: int):
        GB.redis.set_hash(self.process_key, name, json.dumps([time, life]))

    def clear_cache(self):
        GB.redis.delete(self.process_key)

    def set_stop_num(self, num: int):
        self._stop_task_num = num
        GB.redis.set_cache(self.stop_task_num_key, self._stop_task_num)

    def get_stop_num(self) -> (int, int):
        cache = GB.redis.get_cache(self.stop_task_num_key)
        full_num = self._stop_task_num
        if cache is not None:
            full_num = int(cache)
        return full_num, self._stop_task_num

    def set_stop_signal(self):
        self._stop_signal = True

    def check_stop_signal(self):
        if self._stop_signal:
            self._stop_task_num -= 1
            while True:
                time.sleep(3600)
