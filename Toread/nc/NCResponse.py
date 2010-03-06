from Vivaldi import Vivaldi
from Pharos import PHAROS
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
    if data == "PharosBase":
        if DEBUG:
            print "[NCResponse] Get a Pharos base NC request from", host
        globalnc = True
        PHAROS.main.myNbManager.globalNeighborMgr.addIP(host)
        return PHAROS.main.myMsgManager.encodeOne( globalnc, -1 )
    if data == "PharosCluster":
        if DEBUG:
            print "[NCResponse] Get a pharos cluster NC request from", host
        globalnc = False
        PHAROS.main.myNbManager.clusterNeighborMgr.addIP(host)
        return PHAROS.main.myMsgManager.encodeOne( globalnc, -1 )
    if data == "PharosInfo":
        if DEBUG:
            print "[NCResponse] Get a pharos info request from", host
        return PHAROS.main.myMsgManager.encodePharosInfo()
    if data == "getPharosString":
        if DEBUG:
            print "[NCResponse] Get a pharos get string info request from", host
        return PHAROS.main.myMsgManager.encodePharosInfoAsString()    
    return ""