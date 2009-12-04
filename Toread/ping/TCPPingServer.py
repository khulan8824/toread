from twisted.internet import protocol

class TCPPingServerProtocol(protocol.Protocol):
    def dataReceived(self,data):
        self.transport.write(data)

class TCPPingServerFactory(protocol.ServerFactory):
    protocol=TCPPingServerProtocol

