import json
import time

from assiatant import GB
from assiatant.singleton import Singleton


@Singleton
class Info(object):
    _stop_task_num = 0

    def __init__(self):
        self.process_key = GB.config.get("App", "PROJECT") + ':process:board'
        self.stop_signal = GB.config.get("App", "PROJECT") + ':signal:stop'

    def insert_process(self, name, time, life: int):
        GB.redis.set_hash(self.process_key, name, json.dumps([time, life]))

    def clear_cache(self):
        GB.redis.delete(self.process_key)

    @property
    def stop_task_num(self) -> int:
        signal = GB.redis.get_cache(self.stop_signal)
        if signal is not None:
            return int(signal)
        return self._stop_task_num

    @stop_task_num.setter
    def stop_task_num(self, num: int):
        if GB.redis.get_cache(self.stop_signal) is not None:
            return int()
        self._stop_task_num = num
        return self

    def set_stop_signal(self):
        GB.redis.set_cache(self.stop_signal, self.stop_task_num)

    def check_stop_signal(self):
        if GB.redis.get_cache(self.stop_signal) is not None:
            self.stop_task_num -= 1
            while True:
                time.sleep(3600)
