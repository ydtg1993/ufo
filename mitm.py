import re
import mitmproxy.http
from assiatant import GB


def request(flow: mitmproxy.http.HTTPFlow) -> None:
    url = flow.request.host


def response(flow: mitmproxy.http.HTTPFlow) -> None:
    url = flow.request.url
    if re.match(r".*m3u8.*", url):
        GB.redis.set_cache(GB.process_cache_conf['hook_video']['key'], url, 10)
    if re.match(r"^.*upload.*\.jpg", url):
        GB.redis.set_cache(GB.process_cache_conf['hook_cover']['key'], url, 10)
