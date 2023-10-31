import re
import time

import mitmproxy.http
from assiatant import GB
from model.source_video_model import SourceVideoModel


def request(flow: mitmproxy.http.HTTPFlow) -> None:
    url = flow.request.host
    if "fanzafree.com" in url:
        return


def response(flow: mitmproxy.http.HTTPFlow) -> None:
    url = flow.request.url

    if re.match(r".*index.m3u8.*", url):
        GB.redis.set_cache(GB.process_cache_conf['hook_video']['key'], url, 15)
    if re.match(r".*big_cover.*", url):
        GB.redis.set_cache(GB.process_cache_conf['hook_cover']['key'], url, 15)
