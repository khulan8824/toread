from Vivaldi import Vivaldi

def getResponseData(host,data):
    
    if data == "Vivaldi":
        Vivaldi.main.myMananger.addIP(host)
        return Vivaldi.main.messegeManager.encodeGossip(host)
    
    return ""