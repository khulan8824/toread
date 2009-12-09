from PharosMessageManager import PharosMessageManager
from PharosNeighborManager import PharosNeighborManager
from PharosNCClient import PharosNCClient
from ping import whereis_newping
from config import *
from twisted.internet import reactor
from ping import PingClientIF
from gossip import GossipClient
from nc import NCClient
from coor.HeightCoordinate import *
import socket
import sys

class PHAROS():
    def __init__(self):
        self.round = 0
        self.myClient = PharosNCClient()
        self.myNbManager = PharosNeighborManager()
        self.myMsgManager = PharosMessageManager()
        "initiate the nc of myClient"
        tmpCoor = HeightCoordinate()
        self.myClient.globalNC.set(MYIP, tmpCoor, 1.5)
        tmpCoor = HeightCoordinate()
        self.myClient.clusterNC.set(MYIP, tmpCoor, 1.5)        
        
        "this part checks whether myself is in the landmark list or the bootstrap list"
        clusterID = None
        clusterkeys = PHAROS_LM.keys()
        for id in clusterkeys:
            if clusterID!=None:
                break
            lms = PHAROS_LM[id]
            for lm in lms:
                lmip = socket.gethostbyname(lm)
                if lmip==MYIP:
                    clusterID = id
                    break

        '''this part will find the cluster of the node'''
        if clusterID == None:
            clusternames = PHAROS_LM.keys()
            pingResult ={}
            for id in clusternames:
                lms = PHAROS_LM[id]
                pingResult[id] = 5000
                temp = []
                for lm  in lms:
                    lmip = socket.gethostbyname(lm)
                    try:
                        res=int(whereis_newping.pingNode(alive=0, timeout=1.0, ipv6=0, number=3, node=lmip, flood=0, size=whereis_newping.ICMP_DATA_STR))
                    except:
                        continue
                    temp.append(res)
                temp.remove(max(temp))
                temp.remove(min(temp))
                if len(temp)==0:
                    print "Error when locating the cluster ID:",id,"!\n Pharos will exit..."
                    sys.exit(1)
                pingResult[id] = float(sum(temp))/len(temp)
            minrtt = min(pingResult.values())
            clusterID=""
            for id in clusternames:
                if pingResult[id]==minrtt:
                    clusterID = id
                    break
        ''' we store the cluster info in clusterID'''
        self.myClient.clusterID = clusterID
        " initiate the bootstrap list according to the clusterID"
        clusterboot = CLUSTER_BOOTLIST[clusterID]
        for node in clusterboot:
            ip = socket.gethostbyname(node)
            if ip==MYIP:
                continue
            self.myNbManager.clusterNeighborMgr.addIP(ip)
        
        "initiate the boostrap list of the global overlay"
        for node in GLOBAL_BOOTLIST:
            ip = socket.gethostbyname(node)
            if ip==MYIP:
                continue
            self.myNbManager.globalNeighborMgr.addIP(ip)
        
        self.mainloop()
        
    def globalPingFinish(self,pingData):
        self.globalrtt = pingData.time
        if self.globalrtt<PINGTIMEOUT/PINGNUM and self.globalrtt>0:
            NCDefer = NCClient.request("PharosBase",self.globalNBIP,NCPORT,NCTIMEOUT)
            NCDefer.addCallback(self.NCRecieved)  
        return
    
    def localPingFinish(self,pingData):
        self.localrtt = pingData.time
        if self.localrtt<PINGTIMEOUT/PINGNUM and self.localrtt>0:
            NCDefer = NCClient.request("PharosCluster",self.localNBIP,NCPORT,NCTIMEOUT)
            NCDefer.addCallback(self.NCRecieved)  
        return
        
    def GossipRecieved(self,gossipData):
        #translate from messege
        gossipClientList = self.myMsgManager.decodeGossip(gossipData.recv)
        for eachClient in gossipClientList:
            tmpclient = eachClient["client"]
            if tmpclient.getIP()!=MYIP:
                if eachClient["nctype"]=="global":
                    self.myNbManager.globalNeighborMgr.addClient(tmpclient)
                if eachClient["nctype"]=="cluster":
                    if eachClient["clusterID"]!=self.myClient.clusterID:
                        print "Error when updating cluster overlay neighbors, the clusterID is different. Neighbor ip:",tmpclient.getIP()
                    self.myNbManager.clusterNeighborMgr.addClient(tmpclient)
        '''update neighbors'''
        return
    
    def NCRecieved(self,ncData):
        #translate from messege
        targetInfo=self.myMsgManager.decodeOne(ncData.recv)
        targetClient = targetInfo["client"]
        if targetInfo["nctype"]=="global":
            print "Update global:",targetClient.ip,",RTT=",self.globalrtt*1000
            targetNeighbor=self.myNbManager.globalNeighborMgr.getNeighbor(targetClient.ip)
            if targetNeighbor==None:
                targetNeighbor=VivaldiNeighbor(PHAROS_USING_HEIGHT_GLOBAL)
            targetNeighbor.setClient(targetClient)
            targetNeighbor.updateRTT(self.globalrtt)
            self.myNbManager.globalNeighborMgr.addClient(targetClient)
            self.myNbManager.globalNeighborMgr.update(targetNeighbor)
            #gossip
            gossipDefer = GossipClient.request("PharosBase",self.globalNBIP,GOSSIPPORT,GOSSIPTIMEOUT)
            gossipDefer.addCallback(self.GossipRecieved)
            #update
            self.myClient.globalNC.update(targetClient,self.globalrtt*1000) #Attention!self.rtt must be multiplied by 1000
        if targetInfo["nctype"]=="cluster":
            print "Update local:",targetClient.ip,",RTT=",self.localrtt*1000
            targetNeighbor=self.myNbManager.clusterNeighborMgr.getNeighbor(targetClient.ip)
            if targetNeighbor==None:
                targetNeighbor=VivaldiNeighbor(PHAROS_USING_HEIGHT_LOCAL)
            targetNeighbor.setClient(targetClient)
            targetNeighbor.updateRTT(self.localrtt)
            self.myNbManager.clusterNeighborMgr.addClient(targetClient)
            self.myNbManager.clusterNeighborMgr.update(targetNeighbor)
            #gossip
            gossipDefer = GossipClient.request("PharosCluster",self.localNBIP,GOSSIPPORT,GOSSIPTIMEOUT)
            gossipDefer.addCallback(self.GossipRecieved)
            #update
            self.myClient.clusterNC.update(targetClient,self.localrtt*1000) #Attention!self.rtt must be multiplied by 1000            
            
        return
    
    
    def mainloop(self):
        self.round = self.round + 1
        print "update times: "+str(self.round)
        print "global nc info:"
        self.myClient.globalNC.printInfo()
        print "local nc info:"
        self.myClient.clusterNC.printInfo()
        reactor.callLater(0, self.updateGlobal)
        reactor.callLater(PHAROS_LOOP_TIME/2, self.updateLocal)
        reactor.callLater(PHAROS_LOOP_TIME, self.mainloop)
        
    def updateGlocal(self):
        nbip = self.myNbManager.globalNeighborMgr.selectIP()
        print "global neighbor ip: ", nbip
        self.globalNBIP = nbip
        pingDefer = PingClientIF.ping(PINGMETHOD,nbip,PINGPORT,PINGTIMEOUT,PINGNUM,PINGBYTES)
        pingDefer.addCallback(self.globalPingFinish)    
        return
    
    def updateLocal(self):
        nbip = self.myNbManager.clusterNeighborMgr.selectIP()
        print "cluster neighbor ip:",nbip
        self.localNBIP = nbip
        pingDefer = PingClientIF.ping(PINGMETHOD,nbip,PINGPORT,PINGTIMEOUT,PINGNUM,PINGBYTES)
        pingDefer.addCallback(self.localPingFinish)           
        return
        
        
def start():
    global main 
    main = PHAROS()
        
        
            
                
                
        
        