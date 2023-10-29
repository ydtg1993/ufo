import re
import mitmproxy.http
from assiatant import GB

def request(flow: mitmproxy.http.HTTPFlow) -> None:
    url = flow.request.host
    print(url)


def response(flow: mitmproxy.http.HTTPFlow) -> None:
    url = flow.request.url
    match = re.match(r".*index.m3u8.*", url)
    #if not match:
    #    return
    print(url)
    with open('output.txt', 'a') as file:
        file.write(f"Matched URL: {url}\n")

