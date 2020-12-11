from twisted.internet import protocol
from twisted.protocols.basic import NetstringReceiver
import GossipResponse
from Vivaldi import Vivaldi

#class GossipServerProtocol(protocol.Protocol):
class GossipServerProtocol(NetstringReceiver):
    #def dataReceived(self,recvdata):
    def stringReceived(self,recvdata):
        senddata = GossipResponse.getResponseData(self.client,recvdata)
        Vivaldi.main.addGossipReceive()
        print('Gossip received from:', self.client)
        #self.transport.write(senddata)
        self.sendString(senddata)
        
    def connectionMade(self):
        self.client = self.transport.getPeer().host

class GossipServerFactory(protocol.ServerFactory):
    protocol=GossipServerProtocol
