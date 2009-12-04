from twisted.internet import protocol

class UDPPingServer(protocol.DatagramProtocol):
    def datagramReceived(self, data, (host, port)):
        self.transport.write(data, (host, port))
       
