from Vivaldi import Vivaldi
from config import *

def getResponseData(host,data):
    
    if data == "Vivaldi":
        if DEBUG:
            print "[NCResponse] Get a Vivaldi NC request from ",host
        Vivaldi.main.myMananger.addIP(host)
        return Vivaldi.main.messegeManager.encodeOne(-1)
    if data == "getVivaldiString":
        if DEBUG:
            print "[NCResponse] Get a Vivaldi get string request from ",host
        return Vivaldi.main.messegeManager.encodeVivaldiString()     
    return ""
