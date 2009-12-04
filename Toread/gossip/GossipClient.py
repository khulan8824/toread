from twisted.internet import protocol,defer,reactor

class GossipData():
    def __init__(self,send="",host="127.0.0.1",port=11233,timeout=10):
        self.send=send
        self.host=host
        self.port=port
        self.timeout=timeout
        self.recv=""
    

class GossipClientProtocol(protocol.Protocol):

    def __init__(self):
        pass
        
    def sendData(self):
        self.transport.write(self.factory.recvbuff.send)
    
    def connectionMade(self):
        self.sendData()
        
    def dataReceived(self, data):
        self.factory.recvbuff.recv=data
        self.transport.loseConnection()
       
            
class GossipClientFactory(protocol.ClientFactory):
    protocol = GossipClientProtocol
    
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
    recvbuff = GossipData(send,host,port,timeout)
    factory = GossipClientFactory(recvbuff)
    reactor.connectTCP(recvbuff.host,recvbuff.port,factory,recvbuff.timeout)
    d = factory.defer
    reactor.callLater(recvbuff.timeout, factory.stopFactory)         
    return d
