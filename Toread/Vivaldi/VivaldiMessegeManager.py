import pickle
import Vivaldi
from coor.HeightCoordinate import *
from VivaldiNCClient import *
from config import *
'''
class VivaldiNCMessege():
    ip = "127.0.0.1"
    vec = Vivaldi.main.myClient.coor.vec
    height = Vivaldi.main.myClient.coor.height
    error = Vivaldi.main.myClient.error_local
'''

class VivaldiNCMessege():
    ip = ""
    vec = []
    height = 0
    error = 0
    
class VivaldiMessegeManager():
    
    def encodeOne(self,index):
        #for debug
        if index == -2:
            temp = VivaldiNCMessege()
            temp.ip = "127.0.0.1"
            temp.vec = [1,1,1,1]
            temp.height = 1
            temp.error = 1.5
        
        #myself
        if index == -1:
            temp = VivaldiNCMessege()
            temp.ip = MYIP
            temp.vec = Vivaldi.main.myClient.coor.vec
            if VIVALDI_USING_HEIGHT>0:
                temp.height = Vivaldi.main.myClient.coor.height
            temp.error = Vivaldi.main.myClient.error
        
        #for gossip
        if index >= 0:
            temp = VivaldiNCMessege()
            temp.ip = Vivaldi.main.myMananger.neighborList[index].getIP()
            temp.vec = Vivaldi.main.myMananger.neighborList[index].client.coor.vec
            if VIVALDI_USING_HEIGHT>0:
                temp.height = Vivaldi.main.myMananger.neighborList[index].client.coor.height
            temp.error = Vivaldi.main.myMananger.neighborList[index].getError()
        print "Messege Encode: IP=",temp.ip,",vec=",temp.vec,",height=",temp.height
        str = pickle.dumps(temp)
        return str
    
    def decodeOne(self,str):
        data = pickle.loads(str)
        print "Messege Decode: IP=",data.ip,",vec=",data.vec,",height=",data.height
        client = VivaldiNCClient()
        coor = HeightCoordinate()
        coor.setCoor(data.vec,data.height)
        client.set(data.ip,coor,data.error)
        return client
    
    def encodeGossip(self,host):
        list = []
        index=Vivaldi.main.myMananger.upload()
        for i in index:
            list.append(self.encodeOne(i))
        str = pickle.dumps(list)
        return str
        
    def decodeGossip(self,str):
        list = pickle.loads(str)
        result = []
        for eachStr in list:
            result.append(self.decodeOne(eachStr))
        return result
