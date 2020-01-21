#!/usr/bin/python
from datetime import datetime
import threading
import time
import logging

def PrintMsg(msg):
    '''Print message to console with Datetime,
    and write to log file.
    
    Args:
        msg: string
    '''
    
    now = datetime.now() # current date and time
    #write to log file
    date = now.strftime("%m-%d-%Y")
    logging.basicConfig(filename='logs/' + date + '.log',level=logging.DEBUG,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info(msg)

    #show msg to console
    date_time = now.strftime("%Y/%m/%d %H:%M:%S")
    print('[' + date_time + '] ' + msg)
    
