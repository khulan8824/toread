from twisted.internet import reactor
from TCPPingClient import TCPPingClientFactory
from UDPPingClient import UDPPingClient
from config import *

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
        if DEBUG:
            print "[TCP PingClient] begin to connect to ",option.host
        reactor.connectTCP(option.host,option.port,factory,option.timeout)
        if DEBUG:
            print "[TCP PingClient] After connection...."
        d = factory.defer
        reactor.callLater(option.timeout, factory.stopFactory)         
    else:
        protocol = UDPPingClient(option)
        reactor.listenUDP(0, protocol)
        d = protocol.defer
        reactor.callLater(option.timeout, protocol.stopProtocol)        

    return d
