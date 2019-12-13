import threading
import sys
import os

print("Welcome to Angelplayer server!")

print("starting socket server...")
#Load socket server module
import srv_socket
from srv_socket import socket_server_start

print("starting http server...")
#Load http server module
import srv_http
from srv_http import http_server_start

#start http server
t1 = threading.Thread(target = http_server_start)
t1.start()

#start socket server
t2 = threading.Thread(target = socket_server_start)
t2.start()


while True:
    cmd = input()
    if(cmd == 'exit'):
        print("Good Bye!")
        os._exit(0)
    else:
        print("Doesn't exist command: " + cmd)
    
