import json
import os
from http.server import BaseHTTPRequestHandler
from assiatant import GB
from director.info import Info


class Manager(BaseHTTPRequestHandler):
    def do_GET(self):
        token = self.headers.get('secret')
        if token != GB.config.get('Http', 'SECRET'):
            self.send_response(401)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('Unauthorized'.encode('utf-8'))
            return
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        uri = self.path
        script_dir = os.path.dirname(__file__)
        if uri == '/app.css' or uri == '/component.min.css' or uri == '/app.js' or uri == '/component.min.js':
            with open(os.path.join(script_dir, uri.lstrip("/")), 'r', encoding='utf-8') as file:
                content = file.read()
        else:
            with open(os.path.join(script_dir, "index.html"), 'r', encoding='utf-8') as file:
                content = file.read()
        self.wfile.write(content.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = {'code': 0, 'data': {}, 'message': 'success'}
        i = Info()
        try:
            parsed_data = json.loads(post_data)
            if parsed_data['command'] == 'process-board':
                data['data']['process'] = {}
                data['data']['process'] = i.get_process()
                full_num, num = i.get_stop_num()
                data['data']['stop_signal'] = {'full_num': full_num, 'num': num}
                data['data']['current_task'] = i.get_current_task()
                data['data']['process_cache_conf'] = GB.process_cache_conf
            elif parsed_data['command'] == 'process_cache':
                if parsed_data['type'] == 'queue':
                    data['data'] = GB.redis.get_queue(parsed_data['cache'], -201, -1)
                elif parsed_data['type'] == 'hash':
                    keys = GB.redis.get_hash_keys(parsed_data['cache'])
                    data['data'] = []
                    for _, key in enumerate(keys):
                        data['data'].append({'key': key, 'val': GB.redis.get_hash(parsed_data['cache'], key)})
            elif parsed_data['command'] == 'command_stop':
                i.set_stop_signal()

        except json.JSONDecodeError as e:
            data = {'code': 1, 'data': {}, 'message': str(e)}
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
