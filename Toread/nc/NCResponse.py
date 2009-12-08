from Vivaldi import Vivaldi
from Pharos import PHAROS

def getResponseData(host,data):
    
    if data == "Vivaldi":
        print "Get a Vivaldi NC request from ",host
        return Vivaldi.main.messegeManager.encodeOne(-1)
    if data == "PharosBase":
        globalnc = True
        return PHAROS.main.myMsgManager.encodeOne( globalnc, -1 )
    if data == "PharosCluster":
        globalnc = False
        return PHAROS.main.myMsgManager.encodeOne( globalnc, -1 )
    
    return ""