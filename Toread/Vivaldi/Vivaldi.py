from config import *
from twisted.internet import reactor
from ping import PingClientIF
from gossip import GossipClient
from nc import NCClient
from VivaldiNeighborManager import *
from coor.HeightCoordinate import *
from VivaldiMessegeManager import *
import socket

class Vivaldi():
    
    myClient = VivaldiNCClient()
    myMananger = VivaldiNeighborManager()
    messegeManager = VivaldiMessegeManager()
   
    def __init__(self):
        '''init'''
        tmpVec = [5,5,5,5]
        tmpHeight = 2
        tmpCoor = HeightCoordinate()
        tmpCoor.setCoor(tmpVec,tmpHeight)
        self.myClient.set(MYIP, tmpCoor, 1.5)
        for boot in SERVERS:
            bootip = socket.gethostbyname(boot)
            if bootip!=MYIP:
                self.myMananger.addIP(bootip)
        self.round = 0
        self.mainloop();
        
    def PingFinish(self,pingData):
        self.rtt = pingData.time
        print "ping neighbor ", self.neighborIP, " rtt: ",self.rtt
        if self.rtt<PINGTIMEOUT/PINGNUM and self.rtt>0:
            NCDefer = NCClient.request("Vivaldi",self.neighborIP,NCPORT,NCTIMEOUT)
            print "send a NC request to ",self.neighborIP
            NCDefer.addCallback(self.NCRecieved)  
        return

    def GossipRecieved(self,gossipData):
        #translate from messege
        gossipClientList = self.messegeManager.decodeGossip(gossipData.recv)
        for eachClient in gossipClientList:
            if eachClient.getIP()!=MYIP:
                self.myMananger.addClient(eachClient)
        '''update neighbors'''
        return

    def NCRecieved(self,ncData):
        #translate from messege
        targetClient=self.messegeManager.decodeOne(ncData.recv)
        #print "Update:",targetClient.ip,",RTT=",self.rtt*1000
        # this part needs to be modified to use filter
        targetNeighbor=self.myMananger.getNeighbor(targetClient.ip)
        if targetNeighbor==None:
            targetNeighbor = VivaldiNeighbor()
        targetNeighbor.setClient(targetClient)
        targetNeighbor.updateRTT(self.rtt)
        self.myMananger.addClient(targetClient)
        self.myMananger.update(targetNeighbor)
        #gossip
        gossipDefer = GossipClient.request("Vivaldi",self.neighborIP,GOSSIPPORT,GOSSIPTIMEOUT)
        gossipDefer.addCallback(self.GossipRecieved)
        #update
        print "Update:",targetClient.ip,",RTT=",targetNeighbor.mpFilter()*1000
        self.myClient.update(targetClient,targetNeighbor.mpFilter()*1000)
        
        #the following is the old code, which do not use any filter
        #print "Update:",targetClient.ip,",RTT=",self.rtt*1000
        #self.myClient.update(targetClient,self.rtt*1000) #Attention!self.rtt must be multiplied by 1000
        return

    def mainloop(self):
        #Choose a neighbor
        self.round = self.round + 1 # used in log
        print 'Round ' + str(self.round) + ': '    # write in log
        self.myClient.printInfo()
        ip = self.myMananger.selectIP()
        print 'neighborIP = ' + ip  # write in log
        self.neighborIP = ip
        '''
        self.neighborIP = "192.168.1.2"
        self.myClient.coor.printCoor()
        print self.myClient.error
        '''
        #ping
        pingDefer = PingClientIF.ping(PINGMETHOD,ip,PINGPORT,PINGTIMEOUT,PINGNUM,PINGBYTES)
        #pingDefer = PingClientIF.ping(PINGMETHOD,self.neighborIP,PINGPORT,PINGTIMEOUT,PINGNUM,PINGBYTES)
        pingDefer.addCallback(self.PingFinish)
        #Run every LOOPTIME
        reactor.callLater(LOOPTIME,self.mainloop)

def start():
    global main 
    main = Vivaldi()

