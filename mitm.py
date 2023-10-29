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
    match = re.match(r".*index.m3u8.*", url)
    if not match:
        return

    GB.redis.set_cache(GB.process_cache_conf['video']['key'], url, 7)
