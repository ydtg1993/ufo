import json
from assiatant import GB


class Info:
    def __init__(self):
        self.process_key = GB.config.get("App", "PROJECT") + ':process:board'

    def insert_process(self, name, time, life: int):
        GB.redis.set_hash(self.process_key, name, json.dumps([time, life]))

    def clear_cache(self):
        GB.redis.delete(self.process_key)
