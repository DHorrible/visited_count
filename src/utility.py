import re
import json
import http
import http.server as http_server

class HttpHandler(http_server.BaseHTTPRequestHandler):
    def callback(self):
        paths = self._routes.get(self.command)
        if paths is not None:
            short_paths = re.sub(r'\?.*', '', self.path)
            fun = paths.get(short_paths)
            if fun is not None:
                return fun(self)
        return http.HTTPStatus.NOT_FOUND, str.format('The rout was not found ("{0}")', self.path), dict()


    def do_GET(self):
        status, err, data = self.callback()
        data['status'] = 'ok' if status == http.HTTPStatus.OK else str.format('error ({0}): {1}', status, err)
        self.create_response(status, data)


    def do_POST(self):
        status, err, data = self.callback()
        data['status'] = 'ok' if status == http.HTTPStatus.OK else str.format('error ({0}): {1}', status, err)
        self.create_response(status, data)


    def route(self, method, path, callback):
        if hasattr(self, '_routes') == False:
            self._routes = dict()
        paths = self._routes.get(method)
        if paths is None:
            paths = dict()
        paths[path] = callback
        self._routes[method] = paths


    def create_response(self, status, data):
        self.send_response(status)
        self.send_header('content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


class Server:
    def __init__(self, host, port, handler):
        self._host = host
        self._port = port
        self._handler = handler
        self._httpd = http_server.HTTPServer((self._host, self._port), self._handler)


    def get_handler(self):
        return self._handler


    def start(self):
        self._httpd.serve_forever()


    def stop(self):
        self._httpd.server_close()
