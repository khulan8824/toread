from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver
import GossipResponse

class GossipServerProtocol(protocol.Protocol):
#class GossipServerProtocol(LineReceiver):
    def dataReceived(self,recvdata):
        senddata = GossipResponse.getResponseData(self.client,recvdata)
        self.transport.write(senddata)
        
    def connectionMade(self):
        self.client = self.transport.getPeer().host

class GossipServerFactory(protocol.ServerFactory):
    protocol=GossipServerProtocol
