import threading
import sys
import os

#Load socket server module
import srv_socket
from srv_socket import SocketServerStart
#Load http server module
import srv_http
from srv_http import HttpServerStart

from lib_sqlite import DatabaseInit
from lib_logs import PrintMsg

PrintMsg("Starting HTTP server...")
#start http server
t1 = threading.Thread(target = HttpServerStart)
t1.start()
PrintMsg("Starting WebSocket server...")
#start socket server
t2 = threading.Thread(target = SocketServerStart)
t2.start()
#Initialize Database
DatabaseInit()

PrintMsg("Welcome to Angelplayer server!")
while True:
    cmd = input()

    if(cmd == 'exit'):
        PrintMsg("Good Bye!")
        os._exit(0)

    if(cmd == 'list'):
        continue
    
    PrintMsg("Doesn't exist command: " + cmd)
    
