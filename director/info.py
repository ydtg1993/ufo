import json
import time
from datetime import datetime, timedelta

from assiatant import GB
from assiatant.singleton import Singleton


@Singleton
class Info(object):
    _stop_task_num = 0
    _stop_signal = False

    def __init__(self):
        self.process_key = GB.config.get("App", "PROJECT") + ':dashboard:process'
        self.current_task_key = GB.config.get("App", "PROJECT") + ':dashboard:current:task'
        self.stop_task_num_key = GB.config.get("App", "PROJECT") + ':dashboard:stop:task:num'

    def insert_process(self, name, at, life: int):
        GB.redis.set_hash(self.process_key, name, json.dumps([at, life]))

    def get_process(self) -> dict:
        processes = GB.redis.get_hash_keys(self.process_key)
        result = {}
        for _, process in enumerate(processes):
            msg = GB.redis.get_hash(self.process_key, process)
            msg = json.loads(msg)
            live = False
            if datetime.now() - datetime.strptime(msg[0], "%Y-%m-%d %H:%M:%S") <= timedelta(seconds=msg[1]):
                live = True
            result[process] = {'time': msg[0], 'live': live}
        return result

    def insert_current_task(self, name: str, signal: str):
        GB.redis.set_cache(self.current_task_key + ':' + name, signal, 3000000)

    def get_current_task(self) -> list:
        return GB.redis.get_keys_pattern(self.current_task_key + ':*')

    def clear_cache(self):
        GB.redis.delete(self.process_key)
        GB.redis.delete_keys_pattern(self.current_task_key + '*')
        GB.redis.delete(self.stop_task_num_key)

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
