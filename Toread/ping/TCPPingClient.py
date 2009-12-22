from twisted.internet import protocol
from time import time
from twisted.internet import defer
from config import *

class TCPPingClientProtocol(protocol.Protocol):

    def __init__(self):
        if DEBUG:
            print "TCP ping client protocol __init__ ...."
        self.count=0
        self.time=0
        self.sigma = map(chr,range(256))
        
    def sendData(self):
        pid = self.sigma[self.count]
        data = pid+'\x00'*(self.factory.option.bytes-1)
        self.time -= time()
        self.transport.write(data)
    
    def connectionMade(self):
        if DEBUG:
            print "TCP pinger connected...\nBegin to ping neighbor"
        self.sendData()
        
    def dataReceived(self, data):
        if DEBUG:
            print "Receive data from the remote neighbor, Begin to calculate TCP ping time"
        self.time += time()
        self.count += 1
        if self.count<self.factory.option.num:
            self.sendData()
        else:
            self.factory.option.time=self.time/self.factory.option.num
            self.transport.loseConnection()
       
            
class TCPPingClientFactory(protocol.ClientFactory):
    protocol = TCPPingClientProtocol
    
    def __init__(self,option):
        if DEBUG:
            print "TCP ping client factory __init__ ...."
        self.option=option
        self.defer=defer.Deferred()
        self.done=False
    
    def buildProtocol(self, addr):
        if DEBUG:
            print "TCP ping Client factory build protocol...."
        p = self.protocol()
        p.factory = self
        self.p = p
        return p        

    def clientConnectionLost(self, connector, reason):
        print '[TCP ping client factory] Lost connection.  Reason:', reason
        
    def clientConnectionFailed(self, connector, reason):
        print '[TCP ping client factory] Connection failed. Reason:', reason    
    
    def stopFactory(self):
        if self.done==False:
            self.done=True
            try:
                self.p.transport.loseConnection()
            except Exception, exp:
                print "No connection!"
                print "Exception info:",type(exp),exp.args,exp.message
                print exp
            self.defer.callback(self.option)
