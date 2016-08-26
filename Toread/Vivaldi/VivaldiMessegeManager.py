import pickle
import Vivaldi
from coor.HeightCoordinate import *
from VivaldiNCClient import *
from config import *
import os

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

class ProxyMessage():
	ip = ""
	ttfb = 0

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
	if VIVALDI_MESSAGES:
	   print "Messege Encode: IP=",temp.ip,",vec=",temp.vec,",height=",temp.height
        str = pickle.dumps(temp)
        return str
    
    def decodeOne(self,str):
        data = pickle.loads(str)
	if isinstance(data,ProxyMessage):
		msg,typ = decodeProxy(data)
		return msg, typ
	if VIVALDI_MESSAGES:
            print "Messege Decode: IP=",data.ip,",vec=",data.vec,",height=",data.height
        client = VivaldiNCClient()
        if VIVALDI_USING_HEIGHT>0:
            coor = HeightCoordinate(DIMENTION)
            coor.setCoor(data.vec,data.height)
        else:
            coor = EuclideanCoordinate(DIMENTION)
            coor.setCoor(data.vec)
                
        client.set(data.ip,coor,data.error)
        return client, 'normal'
    
    def encodeProxy(self, proxy):
	proxy_route = Vivaldi.main.routeTable[proxy]
	temp = ProxyMessage()
	temp.ip = proxy_route.ip
	temp.ttfb = proxy_route.ttfb
	str = pickle.dumps(temp)
	return str

    def decodeProxy(self, data):
	Vivaldi.main.routeTable.updateTTFB(data.ip,data.ttfb)
	return "{}\t{}".format(data.ip,data.ttfb),'proxy'
		    

    def encodeGossip(self,host):
        list = []
	proxy =Vivaldi.main.routeTable.proxy
	if proxy:
	    list.append(self.encodeProxy(proxy))
        index=Vivaldi.main.myMananger.upload()
        for i in index:
            list.append(self.encodeOne(i))
        str = pickle.dumps(list)
        return str
        
    def decodeGossip(self,str):
        list = pickle.loads(str)
        result = []
        for eachStr in list:
	    decoded,typ = self.decodeOne(eachStr)
	    if typ != 'proxy':
                result.append(decoded)
        return result

    def encodeVivaldiString(self):
        temp = ""
        temp = temp + "ip:" + str(MYIP) + "@SEP@"
        temp = temp + "vec:" + str(Vivaldi.main.myClient.coor.vec) + "@SEP@"
        if VIVALDI_USING_HEIGHT>0:
            temp = temp + "height:" + str(Vivaldi.main.myClient.coor.height) + "@SEP@"
        temp = temp + "err:" + str(Vivaldi.main.myClient.error)
        return temp
