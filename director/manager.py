import json
import os
from http.server import BaseHTTPRequestHandler
from assiatant import GB
from director.info import Info
from model.source_chapter_model import SourceChapterModel
from model.source_comic_model import SourceComicModel


class Manager(BaseHTTPRequestHandler):
    def do_GET(self):
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

            elif parsed_data['command'] == 'command_reset_comic':
                Manager.reset_comic_update_queue()
            elif parsed_data['command'] == 'command_reset_chapter':
                Manager.reset_chapter_img_queue()
            elif parsed_data['command'] == 'command_stop':
                i.set_stop_signal()

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
