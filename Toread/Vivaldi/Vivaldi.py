from config import *
from twisted.internet import reactor
from ping import PingClientIF
from gossip import GossipClient
from nc import NCClient
from VivaldiNeighborManager import *
from coor.HeightCoordinate import *
from coor.EuclideanCoordinate import *
from VivaldiMessegeManager import *
import RoutingTable as rt
import socket
import time
import sys


class Vivaldi():
    
    myClient = VivaldiNCClient()
    myMananger = VivaldiNeighborManager()
    messegeManager = VivaldiMessegeManager()
    if PROXY_MODE:
    	proxiesManager = VivaldiNeighborManager()

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
	print "round,elapsed,mrtt,mdist,mpe,mrpe,proxy_mrtt,proxy_mdist,proxy_mpe,proxy_mrpe"
	self.proxyRouteTable = rt.RoutingTable('proxy_route_table')
	if PROXY_MODE:
	    for ip in PROXIES:
	        self.proxiesManager.addIP(ip)
	with open('monitored_client','w') as f:
	    f.write("round,rtt,distance,error,rerror\n")
	with open('monitored_proxy','w') as f:
	    f.write("round,rtt,distance,error,rerror\n")
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
    

    def proxyPingFinish(self,pingData):
        self.proxy_rtt = pingData.time
        #print "ping neighbor ", self.neighborIP, " rtt: ",self.rtt
        if self.proxy_rtt<PINGTIMEOUT/PINGNUM and self.proxy_rtt>0:
	    proxy_neighbor = self.proxiesManager.getNeighbor(self.proxy_ip)
	    proxy_neighbor.updateRTT(self.proxy_rtt)
	    proxy_neighbor.client.update(self.myClient,proxy_neighbor.mpFilter()*1000)
	    distance = self.myClient.getCoor().getDistance(proxy_neighbor.client.getCoor())
	    if self.proxy_ip not in self.proxyRouteTable.getProxiesIPs():
	    	self.proxyRouteTable.addRoute(self.proxy_ip,distance)
	    else:
		self.proxyRouteTable.updateDistance(self.proxy_ip,distance)
        return

    def GossipRecieved(self,gossipData):
        #translate from messege
	if VIVALDI_MESSAGES:
	   print 'Gossip Received'
        gossipReply = self.messegeManager.decodeGossip(gossipData.recv)
	# If the neighbour is using a proxy he sends me his ttfb
	if gossipReply['ttfb']:
	    for (ip,ttfb,time_from_last_ttfb) in gossipReply['ttfb']:
		if ip != MYIP:
	            self.proxyRouteTable.updateTTFB(ip,ttfb, time_from_last_ttfb)
	# If the are proxy coords on the neighbour with smaller error then
	# i replace mine with those
        if gossipReply['proxies']:
	    proxy_data = gossipReply['proxies']
	    if proxy_data:
	        local_proxy =  self.proxiesManager.getNeighbor(proxy_data.proxy_ip)
	        if local_proxy:
		    local_proxy.client.update(self.myMananger.getNeighbor(proxy_data.client_ip).client,proxy_data.last_rtt)
	gossipClientList = gossipReply['normal']
        for eachClient in gossipClientList:
            if eachClient.getIP()!=MYIP:
                self.myMananger.addClient(eachClient)
        '''update neighbors'''
	# Print info for exp
	neigh = self.myMananger.getNeighbor(MONITORED_CLIENT)
	if neigh:
	    with open('monitored_client','a') as f:
		if neigh.getRTT():	
		    distance = self.myClient.getCoor().getDistance(neigh.client.getCoor())
	            error = abs(distance-neigh.getRTT()[-1]*1000)
		    rerror = abs(distance-neigh.getRTT()[-1]*1000)/(neigh.getRTT()[-1]*1000)
		    f.write("{},{},{},{},{}\n".format(self.round,neigh.getRTT()[-1]*1000,distance,error,rerror))
	neigh = self.proxiesManager.getNeighbor(MONITORED_PROXY)
	if neigh:
	    with open('monitored_proxy','a') as f:
		if neigh.getRTT():	
	            distance = self.myClient.getCoor().getDistance(neigh.client.getCoor())
	            error = abs(distance-neigh.getRTT()[-1]*1000)
		    rerror = abs(distance-neigh.getRTT()[-1]*1000)/(neigh.getRTT()[-1]*1000)
		    f.write("{},{},{},{},{}\n".format(self.round,neigh.getRTT()[-1]*1000,distance,error,rerror))
	if not ME_PROXY:
	    # Update my proxies TTFB
	    self.proxyRouteTable.readTTFB()
	    self.proxyRouteTable.chooseBestProxy()
	    self.proxyRouteTable.store()
        return

    def NCRecieved(self,ncData):
        #translate from messege
        targetClient,_=self.messegeManager.decodeOne(ncData.recv)
        #print "Update:",targetClient.ip,",RTT=",self.rtt*1000
        # this part needs to be modified to use filter
        targetNeighbor=self.myMananger.getNeighbor(targetClient.ip)
        if targetNeighbor==None:
            targetNeighbor = VivaldiNeighbor()
        targetNeighbor.setClient(targetClient)
        targetNeighbor.updateRTT(self.rtt)
        self.myMananger.addClient(targetClient)
        self.myMananger.update(targetNeighbor)
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
        #gossip
	if VIVALDI_MESSAGES:
	   print 'Gossip Request Sent to {}'.format(self.neighborIP)
        gossipDefer = GossipClient.request("Vivaldi",self.neighborIP,GOSSIPPORT,GOSSIPTIMEOUT)
        gossipDefer.addCallback(self.GossipRecieved)
        return

    def calcMPE(self):
	#Calculate Neighbours Median prediction error
	errors = []
	rerrors = []
	rtts = []
	dists = []
	for neigh in self.myMananger.neighborList:
	   dist = self.myClient.getCoor().getDistance(neigh.client.getCoor())
	   if neigh.rtt:
	      rtt = neigh.rtt[-1]
	      err = abs(dist-rtt*1000)
	      rerr = abs(dist-rtt*1000)/(rtt*1000)
	      errors.append(err)
	      rerrors.append(rerr)
	      dists.append(dist)
	      rtts.append(rtt*1000)
	   else:
	      continue
	mpe = self.median(errors)
	mrpe = self.median(rerrors)
	mrtt = self.median(rtts)
	mdist = self.median(dists)
	proxy_errors = []
	proxy_rerrors = []
	proxy_rtts = []
	proxy_dists = []
	for proxy in self.proxiesManager.neighborList:
	   dist = self.myClient.getCoor().getDistance(proxy.client.getCoor())
	   if proxy.rtt:
	      rtt = proxy.rtt[-1]
	      err = abs(dist-rtt*1000)
	      rerr = abs(dist-rtt*1000)/(rtt*1000)
	      proxy_errors.append(err)
	      proxy_rerrors.append(rerr)
	      proxy_dists.append(dist)
	      proxy_rtts.append(rtt*1000)
	   else:
	      continue
	proxy_mpe = self.median(proxy_errors)
	proxy_mrpe = self.median(proxy_rerrors)
	proxy_mrtt = self.median(proxy_rtts)
	proxy_mdist = self.median(proxy_dists)
	print("{},{},{},{},{},{},{},{},{},{}".format(self.round,self.elapsed, mrtt, mdist, mpe, mrpe, proxy_mrtt, proxy_mdist, proxy_mpe, proxy_mrpe))
	
	
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
	if not ME_PROXY:
	    proxy_ip = self.proxiesManager.selectIP()
	    if proxy_ip:
	        self.proxyRouteTable.checkTTFBUpdate()
	        self.proxy_ip = proxy_ip
		proxyPingDefer = PingClientIF.ping(PINGMETHOD,proxy_ip,PINGPORT,PINGTIMEOUT,PINGNUM,PINGBYTES)
		proxyPingDefer.addCallback(self.proxyPingFinish)
        #Run every LOOPTIME
        reactor.callLater(LOOPTIME,self.mainloop)


def start():
    global main
    main = Vivaldi()

