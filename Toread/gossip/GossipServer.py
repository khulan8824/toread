from twisted.internet import protocol
from twisted.protocols.basic import IntNStringReceiver
import GossipResponse

#class GossipServerProtocol(protocol.Protocol):
class GossipServerProtocol(IntNStringReceiver):
    #def dataReceived(self,recvdata):
    def stringReceived(self,recvdata):
        senddata = GossipResponse.getResponseData(self.client,recvdata)
        #self.transport.write(senddata)
        self.sendString(senddata)
        
    def connectionMade(self):
        self.client = self.transport.getPeer().host

class GossipServerFactory(protocol.ServerFactory):
    protocol=GossipServerProtocol
