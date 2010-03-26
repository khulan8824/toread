#! /usr/bin/env python
#coding=utf-8
'''
    this script get the Pharos NC information of myself, and save it
'''
import getPharosRE
import socket
import sys

def vecToStr(vec):
    s = ""
    for v in vec:
        if len(s)==0:
            s = s + str(v)
        else:
            s = s + '\t' + str(v)
    return s


out_file = "../evaluationResult/myPharosNC.nc"
msg="PharosInfo"
myselfname = socket.gethostname()
mync = getPharosRE.getNodeNCObj( myselfname, msg )
if(mync==None):
    print "can not get NC of myself!"
    sys.exit(1)
myglobalvec = mync.globalvec
myglobalvec.append(mync.globalheight)
myclustervec = mync.clustervec
myclustervec.append(mync.clusterheight)
myclusterid = mync.clusterID

# save the result
# Format : "hostname    globalnc    clusterID   clusterNC"
ofh = open(out_file, 'w')
ofh.write(str(myselfname) + '\t' + vecToStr(myglobalvec) + '\t' + str(myclusterid) + '\t' + vecToStr(myclustervec) + '\n')
ofh.close()
