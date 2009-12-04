from twisted.internet.protocol import DatagramProtocol
from time import time
from twisted.internet import defer

class UDPPingClient(DatagramProtocol):
    def __init__(self,option):
        self.option = option
        self.count=0
        self.time=0
        self.done=False
        self.sigma = map(chr,range(256))
        self.defer = defer.Deferred()
    
    def startProtocol(self):
        self.transport.connect(self.option.host, self.option.port)
        self.sendData()

    def sendData(self):
        pid = self.sigma[self.count]
        data = pid+'\x00'*(self.option.bytes-1)
        self.time -= time()
        self.transport.write(data)
#        print "Client send!"
    
    def datagramReceived(self, data, (host, port)):
#        print "client receive"
        self.time += time()
        self.count += 1
        if self.count<self.option.num:
            self.sendData()
        else:
            self.option.time = self.time/self.option.num
#            print PingClientData.Data.time
            self.transport.loseConnection()

    def stopProtocol(self):
        if self.done==False:
            self.done=True
            self.transport.stopListening()
            self.defer.callback(self.option)
    
    def connectionRefused(self):
        if self.done==False:
            self.done=True
            self.transport.stopListening()
            self.defer.callback(self.option)
    

