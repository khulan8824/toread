from Vivaldi import Vivaldi
from Pharos import PHAROS

def getResponseData(host,data):
    
    if data == "Vivaldi":
        Vivaldi.main.myMananger.addIP(host)
        return Vivaldi.main.messegeManager.encodeGossip(host)
    if data == "PharosBase":
        globalnc = True
        PHAROS.main.myNbManager.globalNeighborMgr.addIP(host)
        print "[Gossip Response] Add global NB ",host
        return PHAROS.main.myMsgManager.encodeGossip( globalnc )
    if data == "PharosCluster":
        globalnc = False
        PHAROS.main.myNbManager.clusterNeighborMgr.addIP(host)
        print "[Gossip Response] Add cluster NB ",host
        return PHAROS.main.myMsgManager.encodeGossip( globalnc )        
    
    return ""