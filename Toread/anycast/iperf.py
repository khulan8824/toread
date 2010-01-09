import sys
import os
import socket

def measureBWstr(hostname = "" ):
    try:
        ip = socket.gethostbyname(hostname)
    except:
        print "Get hostname error, host:",hostname
        return None
    measure = "./iperf -f K -t 8 -c " + ip
    proc = os.popen(measure)
    for line in proc.readlines():
        if line.find("KBytes/sec")>=0:
            words = line.split()
            res = words[7]+" "+words[8]
            print "bandwidth to",hostname,":",res
            return res
    return None

def measureBWnum( hostname=""):
    r = measureBWstr(hostname)
    if r==None:
        return None
    return float(r.split()[0])
            
if __name__=="__main__":
    hostname = sys.argv[1]
    bw = measureBWnum(hostname)
    print "Result+10:",str(bw+10)

