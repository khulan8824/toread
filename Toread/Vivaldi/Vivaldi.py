from config import *
from twisted.internet import reactor
from ping import PingClientIF
from gossip import GossipClient
from nc import NCClient
from VivaldiNeighborManager import *
from coor.HeightCoordinate import *
from coor.EuclideanCoordinate import *
from VivaldiMessegeManager import *
import socket
import time
import sys

class Vivaldi():
    
    myClient = VivaldiNCClient()
    myMananger = VivaldiNeighborManager()
    messegeManager = VivaldiMessegeManager()
   
    def __init__(self):
        '''init'''
        tmpVec = []
        for i in range(DIMENTION):
            tmpVec.append(5)
        
        '''if use height'''
        if VIVALDI_USING_HEIGHT>0:
            tmpHeight = 2
            tmpCoor = HeightCoordinate()
            tmpCoor.setCoor(tmpVec,tmpHeight)
        else:
            tmpCoor = EuclideanCoordinate()
            tmpCoor.setCoor(tmpVec)
            
        self.myClient.set(MYIP, tmpCoor, 1.5)
        for boot in SERVERS:
            bootip = socket.gethostbyname(boot)
	    if DEBUG:
	       print bootip
	       print MYIP
            if bootip!=MYIP:
                self.myMananger.addIP(bootip)
        self.round = 0
	self.start_time = time.time()
	self.elapsed = 0
	print "round,elapsed,mrtt,mdist,mpe"
        self.mainloop();
        
    def PingFinish(self,pingData):
        self.rtt = pingData.time
        #print "ping neighbor ", self.neighborIP, " rtt: ",self.rtt
        if self.rtt<PINGTIMEOUT/PINGNUM and self.rtt>0:
            NCDefer = NCClient.request("Vivaldi",self.neighborIP,NCPORT,NCTIMEOUT)
	    if DEBUG:
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
        if DEBUG:
	   print "Update:",targetClient.ip,",RTT=",targetNeighbor.mpFilter()*1000
        self.myClient.update(targetClient,targetNeighbor.mpFilter()*1000)
	distance = self.myClient.getCoor().getDistance(targetClient.getCoor())
	error = abs(distance-self.rtt*1000)/min((self.rtt*1000),distance)
	if DEBUG:
	   # Prints info on neighbour updated this round
	   print "Round:",self.round,",time:",self.elapsed,",NEIGH:",targetClient.ip,",RTT:",self.rtt*1000,",DIST:",distance,"RE:",error
        
        #the following is the old code, which do not use any filter
        #print "Update:",targetClient.ip,",RTT=",self.rtt*1000
        #self.myClient.update(targetClient,self.rtt*1000) #Attention!self.rtt must be multiplied by 1000
	self.calcMPE()
        return

    def calcMPE(self):
	#Calculate Median prediction error
	errors = []
	rtts = []
	dists = []
	for neigh in self.myMananger.neighborList:
	   dist = self.myClient.getCoor().getDistance(neigh.client.getCoor())
	   if neigh.rtt:
	      rtt = neigh.rtt[-1]
	      err = abs(dist-rtt*1000)/min((rtt*1000),dist)
	      errors.append(err)
	      dists.append(dist)
	      rtts.append(rtt*1000)
	   else:
	      continue
	sys.stderr.write(str(errors))
	mpe = self.median(errors)
	mrtt = self.median(rtts)
	mdist = self.median(dists)
	print("{},{},{},{},{}".format(self.round,self.elapsed, mrtt, mdist, mpe))
	
    def median(self, lst):
	lst = sorted(lst)
	if len(lst) < 1:
	   return None
	if len(lst) %2 == 1:
	   return lst[((len(lst)+1)/2)-1]
	else:
	   return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

    def mainloop(self):
        #Choose a neighbor
        self.round = self.round + 1 # used in log
	self.elapsed = "%2.2f"%(time.time() - self.start_time)
	if DEBUG:
	   print 'Round ' + str(self.round) + ' - '+self.elapsed+' s : '    # write in log
           self.myClient.printInfo()
        ip = self.myMananger.selectIP()
	if ip:
           #print 'neighborIP = ' + ip  # write in log
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

