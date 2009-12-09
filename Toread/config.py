'''UESD FOR INIT'''
'''bootstramp hosts:planetlab2.cis.upenn.edu,planetlab2.cs.columbia.edu,planetlab1.georgetown.edu,planetlab2.cs.ucla.edu'''
SERVER_IP = ['158.130.6.253','128.59.20.227','141.161.20.32','131.179.50.72']

import re, urllib2
MYIP = re.search("td>(\d+\.\d+\.\d+\.\d+)</td", urllib2.urlopen("http://whois.ipcn.org").read())
if MYIP:
    MYIP=MYIP.group(1)
else:
    print "Please check your network!"

'''FOR LOG'''
LOG_IN_DETAIL=0

'''USED IN HeightCoordinate'''
DIMENTION = 4
THRESHOLD_HEIGHT = 0.01

'''USED IN VivaldiNCClient'''
VIVALDI_USING_HEIGHT = 1
VIVALDI_ERROR = 1.5
VIVALDI_ERROR_UNCONNECTED = 2
VIVALDI_CE = 0.25
VIVALDI_CC = 0.25

'''UESD IN VivaldiNeighbor'''
VIVALDI_RTT_NUM = 8


'''USED IN VivaldiNeighborManager'''
VIVALDI_MAX_NEIGHBOR_NUM = 200
VIVALDI_SELECTED_NEIGHBOR_NUM = 32
VIVALDI_UPDATE_STRATEGY = 2 #0 means random, 1 means closest, 2 means hybrid
VIVALDI_UPLOAD_NUM = 2

'''USED IN PharosNCClient'''
PHAROS_USING_HEIGHT_GLOBAL = 1
PHAROS_USING_HEIGHT_LOCAL = 1

'''USED IN PharosNeighborManager'''
PHAROS_UPDATE_STRATEGY_GLOBAL = 2
PHAROS_UPDATE_STRATEGY_LOCAL = 2
#PHAROS_USING_HEIGHT = VIVALDI_USING_HEIGHT
#PHAROS_GLOBAL_ERROR = 1.5
#PHAROS_GLOBAL_ERROR = 1.5

'''USED IN PHAROS BOOTSTRAP'''
PHAROS_LM = {"America":["righthand.eecs.harvard.edu","planetlab3.csail.mit.edu","planetlab2.cs.ucla.edu","planetlab2.cs.uiuc.edu","planetlab2.cs.duke.edu"], "Asia":["pl1.pku.edu.cn","csplanetlab2.kaist.ac.kr","planetlab-1.sjtu.edu.cn","planetlab3.ie.cuhk.edu.hk"], "Europe":["mars.planetlab.haw-hamburg.de","planetlab-3.imperial.ac.uk","planetlab1.tlm.unavarra.es","planetlab1.ceid.upatras.gr"] }  # lm and bootlist should have the same cluster ids
CLUSTER_BOOTLIST = {"America":["planetlab3.csail.mit.edu","planetlab2.cs.ucla.edu","planetlab2.cs.uiuc.edu"], "Asia":["pl1.pku.edu.cn","csplanetlab2.kaist.ac.kr","planetlab-1.sjtu.edu.cn"], "Europe":["planetlab-3.imperial.ac.uk","planetlab1.tlm.unavarra.es","planetlab1.ceid.upatras.gr"] }
GLOBAL_BOOTLIST = ["pl1.pku.edu.cn","righthand.eecs.harvard.edu","pl2.planetlab.ics.tut.ac.jp","planetlab2.cs.ucla.edu","planetlab1.tlm.unavarra.es","planetlab-3.imperial.ac.uk"]

"""     pharos debug list nodes
planetlab2.cesnet.cz
planetlab1.aston.ac.uk
mars.planetlab.haw-hamburg.de
planetlab-3.imperial.ac.uk
planetlab1.tlm.unavarra.es
planetlab1.ceid.upatras.gr
planetlab1.elet.polimi.it
planet03.csc.ncsu.edu
planetlab2.csres.utexas.edu
planetlab1.williams.edu
planetlab2.ucsd.edu
righthand.eecs.harvard.edu
planetlab3.csail.mit.edu
planetlab2.cs.ucla.edu
planetlab2.cs.uiuc.edu
planetlab2.cs.duke.edu
planetlab1.koganei.wide.ad.jp
pl2.planetlab.ics.tut.ac.jp
csplanetlab2.kaist.ac.kr
plab2.cs.ust.hk
planetlab3.ie.cuhk.edu.hk
pl1.pku.edu.cn
planetlab-1.sjtu.edu.cn
"""



'''USED IN PHAROS UPDATE LOOPTIME'''
PHAROS_LOOP_TIME = 10  # make sure that PHAROS_LOOP_TIME>2*max(GOSSIPTIMEOUT,NCTIMEOUT,PINGTIMEOUT)

'''USED IN TWISTED'''
ALGORITHM = "PHAROS"
LOOPTIME = 3
PINGMETHOD = "TCP"
PINGPORT = 51232
PINGTIMEOUT = 3.0 #please ensure that PINGTIMEOUT<LOOPTIME and that it's a float
PINGNUM = 3
PINGBYTES = 56
GOSSIPPORT = 51233
NCPORT = 51234
GOSSIPTIMEOUT = 1 #please ensure that GOSSIPTIMEOUT<LOOPTIME
NCTIMEOUT = 1 #please ensure that NCTIMEOUT<LOOPTIME
