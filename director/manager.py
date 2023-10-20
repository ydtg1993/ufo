import json
import os
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer

from assiatant import GB


class Manager(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        uri = self.path
        script_dir = os.path.dirname(__file__)
        if uri == '/app.css':
            with open(os.path.join(script_dir, "app.css"), 'r', encoding='utf-8') as file:
                content = file.read()
        elif uri == '/app.js':
            with open(os.path.join(script_dir, "app.js"), 'r', encoding='utf-8') as file:
                content = file.read()
        else:
            with open(os.path.join(script_dir, "index.html"), 'r', encoding='utf-8') as file:
                content = file.read()
        self.wfile.write(content.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = {'code': 0, 'data': {}, 'message': 'success'}
        try:
            parsed_data = json.loads(post_data)
            if parsed_data['command'] == 'process-board':
                processes = GB.redis.get_hash_keys(GB.config.get("App", "PROJECT") + ':process:board')
                for _, process in enumerate(processes):
                    msg = GB.redis.get_hash(GB.config.get("App", "PROJECT") + ':process:board', process)
                    msg = json.loads(msg)
                    live = False
                    if datetime.now() - datetime.strptime(msg[0], "%Y-%m-%d %H:%M:%S") <= timedelta(seconds=msg[1]):
                        live = True
                    data['data'][process] = {'time': msg[0], 'live': live}
        except json.JSONDecodeError as e:
            data = {'code': 1, 'data': {}, 'message': str(e)}
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
