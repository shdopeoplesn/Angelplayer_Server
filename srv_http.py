import config
HOST = config.HOST
HTTP_PORT = config.HTTP_PORT

import http.server
import socketserver

def http_server_start():
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((HOST, HTTP_PORT), Handler)
    print("HTTP serving at port: ", HTTP_PORT)
    httpd.serve_forever()