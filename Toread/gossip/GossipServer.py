from twisted.internet import protocol
import GossipResponse

class GossipServerProtocol(protocol.Protocol):
    def dataReceived(self,recvdata):
        senddata = GossipResponse.getResponseData(self.client,recvdata)
        self.transport.write(senddata)
        
    def connectionMade(self):
        self.client = self.transport.getPeer().host

class GossipServerFactory(protocol.ServerFactory):
    protocol=GossipServerProtocol
