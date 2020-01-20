#!/usr/bin/python
from datetime import datetime

def PrintMsg(msg):
    now = datetime.now() # current date and time
    date_time = now.strftime("%Y/%m/%d %H:%M:%S")
    print('[' + date_time + '] ' + msg)