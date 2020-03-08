import base64
import json

from websocket_server import WebsocketServer
#Load config variable
from config import HOST
from config import SOCKET_PORT
from config import HTTP_PORT
from config import CLIENT_FILE_PATH
from config import CLIENT_VERSION
#Load libarys
from lib_logs import PrintMsg
from lib_sqlite import UpdateClientStatus
from lib_sqlite import RemoveClientStatus
from lib_sqlite import GetCurrentDevicesList
from lib_sqlite import GetDeviceDetailByCustomId

class Device():
    def __init__(self, id):
        self.id_ = id
        self.cid_ = ""
        self.inbox_ = ""
        self.flag_sent_ = False

global g_devices
g_devices = {}

def SendUpdateInfo():
    comm = {
        "message": "updateinfo",
        "force_update": False,
        "version": CLIENT_VERSION,
        "url": "http://" + HOST + ":" + str(HTTP_PORT) + "/" + CLIENT_FILE_PATH
    }
    return json.dumps(comm)
#Remove Device data from global list g_devices
def RemoveDeviceById(id):
    RemoveClientStatus(g_devices[id].cid_)
    del g_devices[id]

# Called for every client connecting (after handshake)
def NewClient(client, server):
    PrintMsg("New client connected and was given id %d" % client['id'])
    server.send_message(client,SendUpdateInfo())
    #store client's data
    g_devices[client['id']] = Device(client['id'])


# Called for every client disconnecting
def ClientLeft(client, server):
    PrintMsg("Client(%d) disconnected" % client['id'])
    #remove data of disconnected client
    RemoveDeviceById(client['id'])

# Called when a client sends a message
def MessageReceived(client, server, message):
    id = client['id']
    message_base64 = message
    try:
        message = base64.b64decode(message)
        message = message.decode('UTF-8','strict')
    except:
        return
    
    if(message == "GETLIST"):
        #PrintMsg("Client(%d) sent a GETLIST signal." % (client['id']))
        g_devices[id].cid_ = "ControlPanel"
        server.send_message(client,"SYN")
        server.send_message(client,GetCurrentDevicesList())
        server.send_message(client,"ACK")

    if(message.startswith("GETID-")):
        try:
            #PrintMsg("Client(%d) sent a (%s) signal." % (client['id'],message))
            g_devices[id].cid_ = "ControlPanel"
            cid = message[6:]
            server.send_message(client,"SYN")
            server.send_message(client,GetDeviceDetailByCustomId(cid))
            server.send_message(client,"ACK")
        except:
            PrintMsg("GETID error detected!")

    #When end of communication
    if(message == "ACK"):
        #PrintMsg("Client(%d) sent a ACK signal." % (client['id']))
        #PrintMsg("Recived Data: " + str(g_devices[id].inbox_))
        g_devices[id].flag_sent_ = False
        try:
            data = json.loads(base64.b64decode(g_devices[id].inbox_).decode('UTF-8','strict'))
            UpdateClientStatus(data)
            g_devices[id].cid_ = data['cid']
        except:
            PrintMsg("Json parse error while receive ACK signal from client: " + str(id) + "!")
            #print(base64.b64decode(g_devices[id].inbox_).decode('UTF-8','strict'))
            return
    
    #if client flags shows it still send data,then put data to inbox.
    if(g_devices[id].flag_sent_):
        g_devices[id].inbox_ += message_base64

    #When start of communication
    if(message == "SYN"):
        #PrintMsg("Client(%d) sent a SYN signal." % (client['id']))
        g_devices[id].inbox_ = ""
        g_devices[id].flag_sent_ = True
def SocketServerStart():
    server = WebsocketServer(SOCKET_PORT, HOST)
    server.set_fn_new_client(NewClient)
    server.set_fn_client_left(ClientLeft)
    server.set_fn_message_received(MessageReceived)
    server.run_forever()