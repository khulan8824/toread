from twisted.internet import protocol
from tiwsted.protocols.base import LineReceiver
import NCResponse

#class NCServerProtocol(protocol.Protocol):
class NCServerProtocol(LineReceiver):
    #def dataReceived(self,recvdata):
    def LineReceived(self,recvdata):
        senddata = NCResponse.getResponseData(self.client,recvdata)
        self.transport.write(senddata)
        
    def connectionMade(self):
        self.client = self.transport.getPeer().host

class NCServerFactory(protocol.ServerFactory):
    protocol=NCServerProtocol
