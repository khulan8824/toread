import pickle
import PHAROS
from coor.HeightCoordinate import *
from coor.EuclideanCoordinate import *
from PharosNCClient import *
from config import *


class PharosNCMessage():
    ip = ""
    vec = []
    height = 0
    error = 0
    nctype = ""
    clusterID = ""
    


class PharosInfo():
    ip = ""
    globalvec = []
    globalheight = 0
    clustervec = []
    clusterheight = 0
    clusterID = ""
    globalerror = 0
    clustererror = 0


    
class PharosMessageManager():
    
    def encodeOne(self,globalnc ,index):
        #for cluster nc
        if index == -1 and globalnc == False:
            temp = PharosNCMessage()
            temp.ip = MYIP
            temp.vec = PHAROS.main.myClient.clusterNC.coor.vec
            if PHAROS_USING_HEIGHT_LOCAL>0:
                temp.height = PHAROS.main.myClient.clusterNC.coor.height
            temp.error = PHAROS.main.myClient.clusterNC.error
            temp.clusterID = PHAROS.main.myClient.clusterID
            temp.nctype = "cluster"
        
        # for global nc
        if index == -1 and globalnc == True:
            temp = PharosNCMessage()
            temp.ip = MYIP
            temp.vec = PHAROS.main.myClient.globalNC.coor.vec
            if PHAROS_USING_HEIGHT_GLOBAL>0:
                temp.height = PHAROS.main.myClient.globalNC.coor.height
            temp.error = PHAROS.main.myClient.globalNC.error
            temp.clusterID = PHAROS.main.myClient.clusterID
            temp.nctype = "global"
        
        #for gossip
        if index >= 0 and globalnc == False:
            temp = PharosNCMessage()
            mymgr = PHAROS.main.myNbManager.clusterNeighborMgr
            temp.ip = mymgr.neighborList[index].getIP()
            temp.vec = mymgr.neighborList[index].client.coor.vec
            if PHAROS_USING_HEIGHT_LOCAL>0:
                temp.height = mymgr.neighborList[index].client.coor.height
            temp.error = mymgr.neighborList[index].getError()
            temp.clusterID = PHAROS.main.myClient.clusterID
            temp.nctype = "cluster"
            
        if index >= 0 and globalnc == True:
            temp = PharosNCMessage()
            mymgr = PHAROS.main.myNbManager.globalNeighborMgr
            temp.ip = mymgr.neighborList[index].getIP()
            temp.vec = mymgr.neighborList[index].client.coor.vec
            if PHAROS_USING_HEIGHT_GLOBAL>0:
                temp.height = mymgr.neighborList[index].client.coor.height
            temp.error = mymgr.neighborList[index].getError()
            temp.nctype = "global"
        
        if DEBUG:
            print "[PharosMessageManager] Message Encode: IP=",temp.ip,",vec=",temp.vec,",height=",temp.height,",nctype=",temp.nctype
        str = pickle.dumps(temp)
        return str
    
    def decodeOne(self,str):
        data = pickle.loads(str)
        if DEBUG:
            print "[PharosMessageManager] Message Decode: IP=",data.ip,",vec=",data.vec,",height=",data.height,",nctype=",data.nctype
        if data.nctype=="global":
            use_h = PHAROS_USING_HEIGHT_GLOBAL
            _arg_dim = PHAROS_DIMENSION_GLOBAL
        if data.nctype=="cluster":
            use_h = PHAROS_USING_HEIGHT_LOCAL
            _arg_dim = PHAROS_DIMENSION_LOCAL
        client = VivaldiNCClient( use_h, _arg_dim )
        if use_h:
            coor = HeightCoordinate( _arg_dim )
            coor.setCoor(data.vec,data.height)
        else:
            coor = EuclideanCoordinate( _arg_dim )
            coor.setCoor(data.vec)
        client.set(data.ip,coor,data.error)
        return {"client":client, "nctype":data.nctype, "clusterID":data.clusterID}
    
    def encodeGossip(self,globalnc):
        list = []
        if globalnc:
            mymgr = PHAROS.main.myNbManager.globalNeighborMgr
        else:
            mymgr = PHAROS.main.myNbManager.clusterNeighborMgr
            
        index=mymgr.upload()
        for i in index:
            list.append(self.encodeOne(globalnc, i))
        str = pickle.dumps(list)
        return str
        
    def decodeGossip(self,str):
        list = pickle.loads(str)
        result = []
        for eachStr in list:
            result.append(self.decodeOne(eachStr))
        return result
    
    def encodePharosInfo(self):
        myclient = PHAROS.main.myClient
        temp = PharosInfo()
        temp.ip = myclient.getIP()
        temp.clustervec = myclient.clusterNC.coor.vec
        if PHAROS_USING_HEIGHT_GLOBAL>0:
            temp.globalheight = myclient.globalNC.coor.height
        if PHAROS_USING_HEIGHT_LOCAL>0:
            temp.clusterheight = myclient.clusterNC.coor.height

        temp.clustererror = myclient.clusterNC.error
        temp.clusterID = myclient.clusterID
        temp.globalerror = myclient.globalNC.error
        temp.globalvec = myclient.globalNC.coor.vec
        str = pickle.dumps(temp)
        if DEBUG:
            print "[PharosMessageManager] Encode the PharosInfo class. IP:",temp.ip,",global vec:",temp.globalvec,",global height:",temp.globalheight,",global error:",temp.globalerror,", cluster vec:",temp.clustervec,", cluster height:",temp.clusterheight,", cluster error:",temp.clustererror,", cluster ID:",temp.clusterID
        return str
    
    def encodePharosInfoAsString(self):
        myclient = PHAROS.main.myClient
        temp = "ClusterID:" + str(myclient.clusterID) + "@SEP@"
        temp = temp + "ip:" + str(myclient.getIP())+"@SEP@"
        temp = temp +"globalvec:" + str(myclient.globalNC.coor.vec) +"@SEP@"
        if PHAROS_USING_HEIGHT_GLOBAL>0:
            temp = temp + "globalheight:" + str(myclient.globalNC.coor.height) +"@SEP@"
        temp = temp + "clustervec:" + str(myclient.clusterNC.coor.vec)+"@SEP@"
        if PHAROS_USING_HEIGHT_LOCAL>0:
            temp = temp + "clusterheight:" + str(myclient.clusterNC.coor.height) + "@SEP@"

        if DEBUG:
            print "[PharosMessageManager] Encode the Pharos Info String:",temp
        return temp
        


    