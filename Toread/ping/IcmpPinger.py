import os
import string
from config import *
import random

def Ping(ip):
    pingaling = os.popen("ping -q -c5 "+ip,"r")
    words=[]
    data=[]
    rtt = 10000
    while 1:
        line = pingaling.readline()
        if not line: 
            break
        words=string.split(line)
        try:
            if words[0]=="rtt":
                data=string.split(line,'/')
                rtt = string.atof(data[4])
        except:
            continue
    return rtt
