from twisted.internet import protocol,defer,reactor
from config import *

class NCData():
    def __init__(self,send="",host="127.0.0.1",port=11233,timeout=10):
        self.send=send
        self.host=host
        self.port=port
        self.timeout=timeout
        self.recv=""
    

class NCClientProtocol(protocol.Protocol):

    def __init__(self):
        pass
        
    def sendData(self):
        self.transport.write(self.factory.recvbuff.send)
    
    def connectionMade(self):
        if DEBUG:
            print "NCClientProtocol.connectionMade is called...."
        self.sendData()
        
    def dataReceived(self, data):
        self.factory.recvbuff.recv=data
        self.transport.loseConnection()
       
            
class NCClientFactory(protocol.ClientFactory):
    protocol = NCClientProtocol
    
    def __init__(self,recvbuff):
        self.recvbuff=recvbuff
        self.defer=defer.Deferred()
        self.done=False
    
    def buildProtocol(self, addr):
        p = self.protocol()
        p.factory = self
        self.p = p
        return p        

    def stopFactory(self):
        if self.done==False:
            self.done=True
            try:
                self.p.transport.loseConnection()
            except:
                print "No connection!"
            self.defer.callback(self.recvbuff)

def request(send="",host="127.0.0.1",port=11232,timeout=10):
    recvbuff = NCData(send,host,port,timeout)
    factory = NCClientFactory(recvbuff)
    if DEBUG:
        print "nc request to", host
        print "Begin to connect to",host
    reactor.connectTCP(recvbuff.host,recvbuff.port,factory,recvbuff.timeout)
    d = factory.defer
    reactor.callLater(recvbuff.timeout, factory.stopFactory)         
    return d
