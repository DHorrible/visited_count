#from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

import src.init

# class Server:
#     def __init__(self, host, port, handler):
#         self._host = host
#         self._port = port
#         self._handler = handler
#         self._httpd = BaseHTTPServer.HTTPServer((self._host, self._port), self._handler)
#     def start(self):
#         self._httpd.serve_forever()
#     def stop(self):
#         self._httpd.server_close()


# class HttpHandler(http.server.BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/visited_domains':
#             self.get_domains(self)
#     def get_domains(self):
#         pass



def run(host='localhost', port=8080):
    logging.basicConfig(filename="server.log", level=logging.INFO)

    #r = init.cfg()

    # if r == None:
    #     logging.error('Redis has not bean configurated')
    #     return

    # server = Server('localhost', port, HttpHandler)
    # server.start()

run()
