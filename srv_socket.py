#Load config variable
from config import HOST
from config import SOCKET_PORT

from websocket_server import WebsocketServer

class Device():
    def __init__(self, id):
        self.id_ = id


global g_devices
g_devices = []

#Remove Device data from global list g_devices
def RemoveDeviceById(id):
    for element in g_devices:
        if element.id_ == id:
            g_devices.remove(element)

# Called for every client connecting (after handshake)
def NewClient(client, server):
    print("New client connected and was given id %d" % client['id'])
    #store client's data
    g_devices.append(Device(client['id']))


# Called for every client disconnecting
def ClientLeft(client, server):
    print("Client(%d) disconnected" % client['id'])
    #remove data of disconnected client
    RemoveDeviceById(client['id'])
# Called when a client sends a message
def MessageReceived(client, server, message):
    print("Client(%d) said: %s" % (client['id'], message))
    server.send_message_to_all("Client(%d) said: %s" % (client['id'], message))
    
def SocketServerStart():
    server = WebsocketServer(SOCKET_PORT, HOST)
    server.set_fn_new_client(NewClient)
    server.set_fn_client_left(ClientLeft)
    server.set_fn_message_received(MessageReceived)
    server.run_forever()