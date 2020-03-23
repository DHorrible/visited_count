import json
import http
import http.server as http_server

class HttpHandler(http_server.BaseHTTPRequestHandler):
    def callback(self):
        paths = self._routes.get(self.command)
        if paths is not None:
            fun = paths.get(self.path)
            if fun is not None:
                return fun(self)
    def do_GET(self):
        data = self.callback()
        data["status"] = "ok"
        self.create_response(data)
    def do_POST(self):
        self.callback()
        self.create_response({
            "status": "ok"
        })
    def route(self, method, path, callback):
        if hasattr(self, '_routes') == False:
            self._routes = dict()
        paths = self._routes.get(method)
        if paths is None:
            paths = dict()
        paths[path] = callback
        self._routes[method] = paths
    def create_response(self, data):
        self.send_response(200)
        self.send_header('content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

class Server:
    def __init__(self, host, port, handler, log):
        self._host = host
        self._port = port
        self._handler = handler
        self._log = log
        self._httpd = http_server.HTTPServer((self._host, self._port), self._handler)
    def get_handler(self):
        return self._handler
    def start(self):
        self._httpd.serve_forever()
    def stop(self):
        self._httpd.server_close()

