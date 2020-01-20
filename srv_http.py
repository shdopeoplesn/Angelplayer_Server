#Load config variable
from config import HOST
from config import HTTP_PORT
from lib_logs import PrintMsg
import http.server
import socketserver
import os

def HttpServerStart():
    web_dir = os.path.join(os.path.dirname(__file__), 'build')
    os.chdir(web_dir)

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((HOST, HTTP_PORT), Handler)
    PrintMsg("HTTP serving at port: " + str(HTTP_PORT))
    httpd.serve_forever()