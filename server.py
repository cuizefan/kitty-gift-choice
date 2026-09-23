#!/usr/bin/env python3
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', '8000'))
ROOT = os.path.dirname(os.path.abspath(__file__))
latest_gift = '等待确认中...'

MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global latest_gift
        parsed = urlparse(self.path)

        if parsed.path == '/gift-result':
            body = json.dumps({'gift': latest_gift}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        file_path = parsed.path
        if file_path == '/':
            file_path = '/index.html'
        if file_path.startswith('/'):
            file_path = os.path.join(ROOT, file_path.lstrip('/'))

        if not os.path.exists(file_path) or os.path.isdir(file_path):
            if parsed.path in ('/result.html', '/result'):
                file_path = os.path.join(ROOT, 'result.html')
            else:
                self.send_error(404, 'Not Found')
                return

        try:
            with open(file_path, 'rb') as f:
                content = f.read()
        except OSError:
            self.send_error(404, 'Not Found')
            return

        ext = os.path.splitext(file_path)[1].lower()
        content_type = MIME_TYPES.get(ext, 'application/octet-stream')
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        global latest_gift
        parsed = urlparse(self.path)

        if parsed.path == '/save-gift':
            content_length = int(self.headers.get('Content-Length', '0'))
            raw = self.rfile.read(content_length)
            try:
                payload = json.loads(raw.decode('utf-8') or '{}')
            except json.JSONDecodeError:
                payload = {}

            latest_gift = payload.get('gift') or '等待确认中...'
            body = json.dumps({'gift': latest_gift}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(404, 'Not Found')

    def log_message(self, format, *args):
        return


if __name__ == '__main__':
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'Serving on http://0.0.0.0:{PORT}')
    server.serve_forever()
