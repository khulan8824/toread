from twisted.internet import reactor
from TCPPingClient import TCPPingClientFactory
from UDPPingClient import UDPPingClient

class Option():
    def __init__(self,host,port,method,timeout,num,bytes,time):
        self.host = host
        self.port = port
        self.method = method
        self.timeout = timeout
        self.num = num
        self.bytes = bytes
        self.time = time   

def ping(method="TCP",host="127.0.0.1",port=11232,timeout=10,num=5,bytes=56):
    option = Option(host,port,method,timeout,num,bytes,timeout/num)
    if method=="TCP":
        factory = TCPPingClientFactory(option)
        reactor.connectTCP(option.host,option.port,factory,option.timeout)
        d = factory.defer
        reactor.callLater(option.timeout, factory.stopFactory)         
    else:
        protocol = UDPPingClient(option)
        reactor.listenUDP(0, protocol)
        d = protocol.defer
        reactor.callLater(option.timeout, protocol.stopProtocol)        

    return d
