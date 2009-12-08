from Vivaldi import Vivaldi
from Pharos import PHAROS

def getResponseData(host,data):
    
    if data == "Vivaldi":
        Vivaldi.main.myMananger.addIP(host)
        return Vivaldi.main.messegeManager.encodeGossip(host)
    if data == "PharosBase":
        globalnc = True
        return PHAROS.main.myMsgManager.encodeGossip( globalnc )
    if data == "PharosCluster":
        globalnc = False
        return PHAROS.main.myMsgManager.encodeGossip( globalnc )        
    
    return ""