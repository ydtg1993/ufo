import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


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
        else:
            with open(os.path.join(script_dir, "index.html"), 'r', encoding='utf-8') as file:
                content = file.read()
        self.wfile.write(content.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            parsed_data = json.loads(post_data)
            print(parsed_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {str(e)}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Data received and processed successfully"}).encode('utf-8'))

    def do_PUT(self):
        self.send_response(200)
        self.end_headers()
