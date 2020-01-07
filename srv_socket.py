#Load config variable
from config import HOST
from config import SOCKET_PORT

from websocket_server import WebsocketServer
import base64

class Device():
    def __init__(self, id):
        self.id_ = id
        self.inbox_ = ""
        self.cid_ = ""
        self.ip_ = ""
        self.mac_ = ""
        self.name_ = ""
        self.os_ = ""
        self.user = ""
        self.apps_ = ""
        self.string = ""
        self.flag_sent_ = False



global g_devices
g_devices = {}

#Remove Device data from global list g_devices
def RemoveDeviceById(id):
    del g_devices[id]

# Called for every client connecting (after handshake)
def NewClient(client, server):
    print("New client connected and was given id %d" % client['id'])
    #store client's data
    g_devices[client['id']] = Device(client['id'])


# Called for every client disconnecting
def ClientLeft(client, server):
    print("Client(%d) disconnected" % client['id'])
    #remove data of disconnected client
    RemoveDeviceById(client['id'])

# Called when a client sends a message
def MessageReceived(client, server, message):
    print("Received Raw Data: " + message)
    #decode received message from base64 and turn into UTF-8
    message = base64.b64decode(message).decode('UTF-8','strict')
    #get client's id(Socket Session)
    id = client['id']
    if(message == "GET"):
        print("Client(%d) sent a GET signal." % (client['id']))
        for index in g_devices:
            server.send_message(client,g_devices[index].cid_)
    #When end of communication
    if(message == "ACK"):
        print("Client(%d) sent a ACK signal." % (client['id']))
        #print("Recived Data: " + g_devices[id].inbox_)
        g_devices[id].flag_sent_ = False
        g_devices[id].string_ = g_devices[id].inbox_
        data = g_devices[id].inbox_.split(':')
        g_devices[id].cid_ = data[0]
        g_devices[id].ip_ = data[1]
        g_devices[id].mac_ = data[2]
        g_devices[id].name_ = data[3]
        g_devices[id].os_ = data[4]
        g_devices[id].user_ = data[5]
        g_devices[id].apps_ = data[6]
        print("Received Data from %s (%s)" % (g_devices[id].cid_,g_devices[id].ip_))

    #When start of communication
    if(message == "SYN"):
        print("Client(%d) sent a SYN signal." % (client['id']))
        g_devices[id].inbox_ = ""
        g_devices[id].flag_sent_ = True
    else:
        #if client flags shows it still send data,then put data to inbox.
        if(g_devices[id].flag_sent_):
            g_devices[id].inbox_ += message

def SocketServerStart():
    server = WebsocketServer(SOCKET_PORT, HOST)
    server.set_fn_new_client(NewClient)
    server.set_fn_client_left(ClientLeft)
    server.set_fn_message_received(MessageReceived)
    server.run_forever()