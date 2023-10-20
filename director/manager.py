import json
import os
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler
from assiatant import GB
from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel


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
            elif parsed_data['command'] == 'command_reset_comic':
                Manager.reset_comic_update_queue()
            elif parsed_data['command'] == 'command_reset_chapter':
                Manager.reset_chapter_img_queue()
        except json.JSONDecodeError as e:
            data = {'code': 1, 'data': {}, 'message': str(e)}
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    @staticmethod
    def reset_comic_update_queue():
        batch_size = 500
        offset = 0
        tasks = GB.redis.get_queue(GB.config.get("App", "PROJECT") + ":chapter:task", 0, -1)
        while True:
            results = GB.mysql.session.query(SourceComicModel.id).filter(
                SourceComicModel.source_chapter_count != SourceComicModel.chapter_count).offset(
                offset).limit(
                batch_size).all()
            for result in results:
                tasks.append(str(result[0]))
            tasks = list(set(tasks))
            offset += batch_size
            if len(results) < batch_size:
                GB.redis.delete(GB.config.get("App", "PROJECT") + ":chapter:task")
                for _, comic_id in enumerate(tasks):
                    GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":chapter:task", comic_id)
                break

    @staticmethod
    def reset_chapter_img_queue():
        batch_size = 500
        offset = 0
        tasks = GB.redis.get_queue(GB.config.get("App", "PROJECT") + ":img:task", 0, -1)
        while True:
            results = GB.mysql.session.query(SourceChapterModel.id).filter(
                SourceChapterModel.img_count == 0).offset(offset).limit(
                batch_size).all()
            for result in results:
                tasks.append(str(result[0]))
            tasks = list(set(tasks))
            offset += batch_size
            if len(results) < batch_size:
                GB.redis.delete(GB.config.get("App", "PROJECT") + ":img:task")
                for _, chapter_id in enumerate(tasks):
                    GB.redis.enqueue(GB.config.get("App", "PROJECT") + ":img:task", chapter_id)
                break
