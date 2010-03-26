#! /usr/bin/env python
#coding=utf-8
'''
    this script collects all the rtt information about the host on planetlab
'''
import getPharosRE
import random
import socket

inputfile = "../../myPLnodes.txt"

hosts = getPharosRE.loadHost( inputfile )
# shuffle the host, make sure the traffic is not converge to one node at the same time
random.shuffle(hosts)
myselfname = socket.gethostname()
rtt = {}
if getPharosRE.TCP==True:
    myping = getPharosRE.tcpPing
else:
    myping = getPharosRE.udpPing

r = 0
for h  in hosts:
    if h==myselfname:
        k = myselfname + "->" + h
        rtt[k] = 0
        continue
    r = 0 
    r = myping(h)
    if (r == -100):
        print "ping ",h," Error!"
        continue
    k = myselfname + "->" + h
    rtt[k] = r

out_file = "../evaluationResult/RTTinfo"
# save the result
# Format : "hostname    RTT"
ofh = open(out_file, 'w')
for k in rtt.keys():
    ofh.write(str(k) + '\t' + str(rtt[k]) + '\n')
ofh.close()
