#!/usr/bin/python
from lib_logs import PrintMsg
from config import DB_PATH
import sqlite3
import json

def DatabaseInit():
    '''Initialize the database
    it will connect to data.db,
    and try drop CURRENT_DEVICES table,
    then create new one.

    Return:
        return false if error ocurred
    '''

    try:
        conn = sqlite3.connect(DB_PATH)
        PrintMsg("Opened database successfully")
    except:
        PrintMsg("database open failed")
        return False

    try:
        c = conn.cursor()
        c.execute("DROP TABLE CURRENT_DEVICES;")
        PrintMsg("Table CURRENT_DEVICES DROP successfully!")
        conn.commit()
    except:
        PrintMsg("Table CURRENT_DEVICES was not found,creating one now...")
    
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE CURRENT_DEVICES
            (   CID         VARCHAR(50) PRIMARY KEY   NOT NULL,
                IPV4        VARCHAR(50)               NULL,
                MAC         VARCHAR(50)               NULL,
                DEVICE_NAME VARCHAR(50)               NULL,
                OS          VARCHAR(50)               NULL,
                CPU         VARCHAR(50)               NULL,
                MEM         DOUBLE                    NULL,
                CPU_USAGE   DOUBLE                    NULL,
                MEM_REMAIN  DOUBLE                    NULL,
                USER_NAME   VARCHAR(50)               NULL,
                APPS        JSON                      NULL,
                PROCESS     JSON                      NULL,
                DISKS       JSON                      NULL,
                DISKS_USAGE DOUBLE                    NULL
                );''')
        PrintMsg("Table CURRENT_DEVICES created successfully!")
        conn.commit()
    except:
        PrintMsg("Table CURRENT_DEVICES create faild!")
        return False
    conn.close()


def UpdateClientStatus(data):
    '''Update Client's data to MySQLite Table CURRENT_DEVICES
    Args:
        data: json format,parse from srv_cocket.py
    Return:
        retrun False if error occured
    '''
    cid = data["cid"]
    ipv4 = data["ipv4"]
    mac = data["mac"]
    device_name = data["device_name"]
    os = data["os"]
    cpu = data["cpu"]
    mem = data["mem"]
    cpu_usage = data["cpu_usage"]
    mem_remain = data["mem_remain"]
    user_name = data["user_name"]
    apps = json.dumps(data["apps"])
    process = json.dumps(data["process"])
    disks = json.dumps(data["disks"])
    disks_usage = data["disks_usage"]

    stored = False

    #connect to DB
    try:
        conn = sqlite3.connect(DB_PATH)
    except:
        PrintMsg("Fail to open database!(UpdateClientStatus)")
        return False
    
    #check if client's data inserted.
    try:
        c = conn.cursor()
        c.execute(f"SELECT * FROM CURRENT_DEVICES WHERE CID = '{cid}'")
        results = c.fetchall()
        if len(results) > 0: stored = True
    except:
        print("Error: unable to fecth data")
        conn.close()
        return False
    
    #if client's data stored, update it.
    if stored:
        try:
            c = conn.cursor()
            c.execute(f"""UPDATE CURRENT_DEVICES SET
            IPV4 = '{ipv4}',
            MAC = '{mac}',
            DEVICE_NAME = '{device_name}',
            OS = '{os}',
            CPU = '{cpu}',
            MEM = {mem},
            CPU_USAGE = {cpu_usage},
            MEM_REMAIN = {mem_remain},
            USER_NAME = '{user_name}',
            APPS = '{apps}',
            PROCESS = '{process}',
            DISKS = '{disks}',
            DISKS_USAGE = '{disks_usage}' WHERE CID = '{cid}'
            ;""")
            #PrintMsg(f"updated {cid}'s data to CURRENT_DEVICES.")
            conn.commit()
        except Exception as e:
            PrintMsg(f"update {cid}'s data to CURRENT_DEVICES faild!")
            PrintMsg("ERROR: " + str(e))
            conn.close()
            return False
    
    #if client's data is not stored,insert it.
    if stored is False:
        try:
            c = conn.cursor()
            c.execute(f"""INSERT INTO CURRENT_DEVICES
            (CID,IPV4,MAC,DEVICE_NAME,OS,CPU,MEM,CPU_USAGE,MEM_REMAIN,USER_NAME,APPS,PROCESS,DISKS,DISKS_USAGE) VALUES 
            ('{cid}','{ipv4}','{mac}','{device_name}','{os}','{cpu}',{mem},{cpu_usage},{mem_remain},'{user_name}','{apps}','{process}','{disks}','{disks_usage}');
            """)
            PrintMsg(f"Insert {cid}'s data to CURRENT_DEVICES successfully!")
            conn.commit()
        except Exception as e:
            PrintMsg(f"Insert {cid}'s data to CURRENT_DEVICES create faild!")
            PrintMsg("ERROR: " + str(e))
            conn.close()
            return False
    conn.close()


def RemoveClientStatus(cid):
    '''Remove Client's data from MySQLite Table CURRENT_DEVICES
    Args:
        cid: string,client's Custom ID
    Return:
        retrun False if error occured
    '''

    #connect to DB
    try:
        conn = sqlite3.connect(DB_PATH)
    except:
        PrintMsg("Fail to open database!(RemoveClientStatus)")
        return False
    
    try:
        c = conn.cursor()
        c.execute(f"DELETE FROM CURRENT_DEVICES WHERE CID = '{cid}'")
        conn.commit()
    except:
        print("Error: unable to delete data(RemoveClientStatus)")
        conn.close()
        return False


def GetCurrentDevicesList():
    '''Get all devices from CURRENT_DEVICES

    Return:
        json,if error ocurred returns null.
    '''
    device_list = []

    #connect to DB
    try:
        conn = sqlite3.connect(DB_PATH)
    except:
        PrintMsg("Fail to open database!(GetCurrentDevicesList)")
        return json.dumps(device_list)
    
    try:
        c = conn.cursor()
        c.execute("SELECT CID,DEVICE_NAME FROM CURRENT_DEVICES")
        results = c.fetchall()
        for device in results:
            tmp = {
            "cid": device[0],
            "device_name": device[1],
            }
            device_list.append(tmp)
    except:
        print("Error: unable to fecth data(GetCurrentDevicesList)")
        conn.close()
    return json.dumps(device_list)

def GetDeviceDetailByCustomId(cid):
    '''Get device detail info from CURRENT_DEVICES by custom id.

    Return:
        json,if error ocurred returns null.
    '''
    device_list = []

    #connect to DB
    try:
        conn = sqlite3.connect(DB_PATH)
    except:
        PrintMsg("Fail to open database!(GetDeviceDetailByCustomId)")
        return json.dumps(device_list)
    
    try:
        c = conn.cursor()
        c.execute(f"""SELECT 
        IPV4,
        MAC,
        DEVICE_NAME,
        OS,
        CPU,
        MEM,
        CPU_USAGE,
        MEM_REMAIN,
        USER_NAME,
        APPS,
        PROCESS,
        DISKS,
        DISKS_USAGE FROM CURRENT_DEVICES WHERE CID = '{cid}'
        ;""")
        results = c.fetchall()
        for device in results:
            tmp = {
            "cid": cid,
            "ipv4": device[0],
            "mac": device[1],
            "device_name": device[2],
            "os": device[3],
            "cpu": device[4],
            "mem": device[5],
            "cpu_usage": device[6],
            "mem_remain": device[7],
            "user_name": device[8],
            "apps": device[9],
            "process": device[10],
            "disks": device[11],
            "disks_usage": device[12]
            }
            device_list.append(tmp)
    except:
        print("Error: unable to fecth data(GetDeviceDetailByCustomId)")
        conn.close()
    return json.dumps(device_list)

    