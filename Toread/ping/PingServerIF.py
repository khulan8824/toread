from twisted.internet import reactor
import TCPPingServer,UDPPingServer

def serv(method="TCP",port=11232):
    if method == "TCP":
        reactor.listenTCP(port,TCPPingServer.TCPPingServerFactory())
    else:
        reactor.listenUDP(port, UDPPingServer.UDPPingServer())
