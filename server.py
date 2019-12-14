import threading
import sys
import os

print("Welcome to Angelplayer server!")

print("starting socket server...")
#Load socket server module
import srv_socket
from srv_socket import SocketServerStart

print("starting http server...")
#Load http server module
import srv_http
from srv_http import HttpServerStart

#start http server
t1 = threading.Thread(target = HttpServerStart)
t1.start()

#start socket server
t2 = threading.Thread(target = SocketServerStart)
t2.start()


from srv_socket import g_devices
while True:
    cmd = input()
    
    if(cmd == 'exit'):
        print("Good Bye!")
        os._exit(0)

    if(cmd == 'list'):
        print(g_devices)
        continue   
    print("Doesn't exist command: " + cmd)
    
