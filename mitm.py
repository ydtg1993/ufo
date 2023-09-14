import re
import mitmproxy.http
from assiatant import GB

print(GB)

def request(flow: mitmproxy.http.HTTPFlow) -> None:
    url = flow.request.host
    if "www.reuters.com" in url:
        return


def response(flow: mitmproxy.http.HTTPFlow) -> None:
    url = flow.request.url
    match = re.match(r".*/rest/v2/playlist/assets.*", url)
    if not match:
        return

    with open('output.txt', 'a') as file:
        file.write(f"Matched URL: {url}\n")

