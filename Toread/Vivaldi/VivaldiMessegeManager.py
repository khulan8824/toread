import jsonpickle
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

class VivaldiProxyMessage():
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
        #mystr = jsonpickle.encode(temp)
        #mystr = temp
	mystr = pickle.dumps(temp)
	return mystr
    
    def decodeOne(self,mystr):
        #data = jsonpickle.decode(mystr)
	data = pickle.loads(mystr)
	#data = mystr
	if isinstance(data,ProxyMessage):
		msg,typ = self.decodeProxy(data)
		return msg, typ
	if isinstance(data,VivaldiProxyMessage):
		msg,typ = self.decodeProxyOne(data)
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
    
    def encodeProxies(self):
	msgs = []
	for proxy in Vivaldi.main.proxiesManager.neighborList:
	    temp = VivaldiProxyMessage()
	    temp.ip = proxy.getIP()
	    temp.vec = proxy.client.coor.vec
	    if VIVALDI_USING_HEIGHT>0:
	        temp.height = proxy.client.coor.height
	    temp.error = proxy.getError()
	    if VIVALDI_MESSAGES:
	        print "Vivaldi Proxy Message Encode IP=", temp.ip,", vec", temp.vec, ",height", temp.height
	    #str = jsonpickle.encode(temp)
	    #mystr = temp
	    mystr = pickle.dumps(temp)
	    msgs.append(mystr)
        return msgs

    def encodeProxy(self, proxy):
        proxy_route = Vivaldi.main.routeTable.getRoute(proxy)
	temp = ProxyMessage()
	temp.ip = proxy_route.ip
	temp.ttfb = proxy_route.ttfb
	if VIVALDI_MESSAGES:
	    print "TTFB Proxy Message Encode: IP=",temp.ip,",TTFB=",temp.ttfb
        #str = jsonpickle.encode(temp)
	#mystr = temp
	mystr = pickle.dumps(temp)
	return mystr

    def decodeProxy(self, data):
	if VIVALDI_MESSAGES:
            print "TTFB Proxy Message Decode: IP=",data.ip,",TTFB=",data.ttfb
	return (data.ip,data.ttfb),'ttfb'
		    
    def decodeProxyOne(self, data):
        client = VivaldiNCClient()
        if VIVALDI_USING_HEIGHT>0:
            coor = HeightCoordinate(DIMENTION)
            coor.setCoor(data.vec,data.height)
        else:
            coor = EuclideanCoordinate(DIMENTION)
            coor.setCoor(data.vec)
	if VIVALDI_MESSAGES:
	    print "Vivaldi Proxy Message Decode IP=", data.ip,", vec", data.vec, ",height", data.height
        client.set(data.ip,coor,data.error)
        return client, 'proxies'

    def encodeGossip(self,host):
        mylist = []
	# If using a proxy share the TTFB of the proxy with the others
	if host not in Vivaldi.main.routeTable.getProxiesIPs():
	    proxy = Vivaldi.main.routeTable.getProxy()
	    if proxy:
	        mylist.append(self.encodeProxy(proxy))
	# If measuring in external procy coordinates share them
	if PROXY_MODE:
		mylist.extend(self.encodeProxies())
	# Normal vivaldi gossip messages
        index=Vivaldi.main.myMananger.upload()
        for i in index:
            mylist.append(self.encodeOne(i))
        mystr = jsonpickle.encode(mylist)
        return mystr
        
    def decodeGossip(self,mystr):
        mylist = jsonpickle.decode(mystr)
	result = {'normal':[],'ttfb':[],'proxies':[]}
        for eachStr in mylist:
	    decoded,typ = self.decodeOne(eachStr)
            result[typ].append(decoded)
        return result

    def encodeVivaldiString(self):
        temp = ""
        temp = temp + "ip:" + str(MYIP) + "@SEP@"
        temp = temp + "vec:" + str(Vivaldi.main.myClient.coor.vec) + "@SEP@"
        if VIVALDI_USING_HEIGHT>0:
            temp = temp + "height:" + str(Vivaldi.main.myClient.coor.height) + "@SEP@"
        temp = temp + "err:" + str(Vivaldi.main.myClient.error)
        return temp
