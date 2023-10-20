from http.server import HTTPServer
from assiatant import GB
from director.manager import Manager


class HttpService:
    def __init__(self):
        http_server = HTTPServer((GB.config.get("Http", "HOST"), int(GB.config.get("Http", "PORT"))), Manager)
        http_server.serve_forever()
