from twisted.internet import protocol
import NCResponse

class NCServerProtocol(protocol.Protocol):
    def dataReceived(self,recvdata):
        senddata = NCResponse.getResponseData(self.client,recvdata)
        self.transport.write(senddata)
        
    def connectionMade(self):
        self.client = self.transport.getPeer().host

class NCServerFactory(protocol.ServerFactory):
    protocol=NCServerProtocol
