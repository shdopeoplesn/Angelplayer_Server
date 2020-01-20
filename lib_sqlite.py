#!/usr/bin/python
from lib_logs import PrintMsg

import sqlite3

def DatabaseInit():
    try:
        conn = sqlite3.connect('data.db')
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
            (CID         VARCHAR(50) PRIMARY KEY   NOT NULL,
                IPV4        VARCHAR(50)               NULL,
                MAC         VARCHAR(50)               NULL,
                DEVICE_NAME VARCHAR(50)               NULL,
                OS          VARCHAR(50)               NULL,
                USER_NAME   VARCHAR(50)               NULL,
                APPS        TEXT                      NULL,
                PROCESS     TEXT                      NULL,
                STRING      TEXT                      NULL
                );''')
        PrintMsg("Table CURRENT_DEVICES created successfully!")
        conn.commit()
    except:
        PrintMsg("Table CURRENT_DEVICES create faild!")
        return False
    conn.close()