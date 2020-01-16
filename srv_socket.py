#Load config variable
from config import HOST
from config import SOCKET_PORT

from websocket_server import WebsocketServer
import base64
import json

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
        self.process = ""
        self.string_ = ""
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
    #print("Received Raw Data: " + message)

    #decode received message from base64 and turn into UTF-8
    message = base64.b64decode(message).decode('UTF-8','strict')

    #print("Received decoded Data: " + message)
    #get client's id(Socket Session)
    id = client['id']

    if(message == "GETLIST"):
        print("Client(%d) sent a GETLIST signal." % (client['id']))
        g_devices[id].cid_ = "ControlPanel"
        device_list = []
        server.send_message(client,"SYN")

        for index in g_devices:
            if g_devices[index].cid_ is "ControlPanel" or g_devices[index].cid_ is "":
                continue
            tmp = {
            "sid": index,
            "cid": g_devices[index].cid_,
            "device_name": g_devices[index].device_name_,
            }
            device_list.append(tmp)

        server.send_message(client,json.dumps(device_list))
        server.send_message(client,"ACK")

    if(message.startswith("GETID-")):
        print("Client(%d) sent a (%s) signal." % (client['id'],message))
        device_list = []
        g_devices[id].cid_ = "ControlPanel"
        sid = message[6:]
        server.send_message(client,"SYN")
        for index in g_devices:
            if str(index) == sid:
                device_list.append(json.loads(g_devices[index].string_))

        server.send_message(client,json.dumps(device_list))
        server.send_message(client,"ACK")

    #When end of communication
    if(message == "ACK"):
        print("Client(%d) sent a ACK signal." % (client['id']))
        #print("Recived Data: " + g_devices[id].inbox_)
        g_devices[id].flag_sent_ = False
        g_devices[id].string_ = g_devices[id].inbox_
        data = j = json.loads(g_devices[id].inbox_)
        g_devices[id].cid_ = data["cid"]
        g_devices[id].ipv4_ = data["ipv4"]
        g_devices[id].mac_ = data["mac"]
        g_devices[id].device_name_ = data["device_name"]
        g_devices[id].os_ = data["os"]
        g_devices[id].cpu_ = data["cpu"]
        g_devices[id].mem_ = data["mem"]
        g_devices[id].cpu_usage_ = data["cpu_usage"]
        g_devices[id].mem_remain_ = data["mem_remain"]
        g_devices[id].user_name_ = data["user_name"]
        g_devices[id].apps_ = data["apps"]
        g_devices[id].process_ = data["process"]
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