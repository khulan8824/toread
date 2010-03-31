'''Get the ip of myself'''
import getSelfIP
import re, urllib2
import sys

MYIP = None
try:
    MYIP = re.search("td>(\d+\.\d+\.\d+\.\d+)</td", urllib2.urlopen("http://whois.ipcn.org").read())
    if MYIP:
        MYIP=MYIP.group(1)    
except:
    ip_proxy = getSelfIP.getSelfIP()
    MYIP = ip_proxy.getip()

if MYIP==None:
    print "Please check your network!"
    print "exit..." 
    sys.exit(1)   

#print "myIP:",MYIP

'''UESD FOR INIT'''
'''bootstramp hosts, we can use ip or hostname in the following list'''
#SERVERS = ['132.239.17.225','202.112.8.2','195.113.161.83','131.179.50.72']
SERVERS = ["planetlab2.ucsd.edu","pl1.pku.edu.cn","planetlab2.cesnet.cz","planetlab2.cs.ucla.edu"]

'''FOR LOG'''
LOG_IN_DETAIL=0

'''USED IN HeightCoordinate'''
DIMENTION = 8
THRESHOLD_HEIGHT = 0.01

'''USED IN VivaldiNCClient'''
VIVALDI_USING_HEIGHT = 1
VIVALDI_ERROR = 1.5
VIVALDI_ERROR_UNCONNECTED = 2
VIVALDI_CE = 0.25
VIVALDI_CC = 0.25

'''UESD IN VivaldiNeighbor'''
VIVALDI_RTT_NUM = 8
#VIVALDI_RTT_NUM = 4
MP_PENCENTILE = 0.25  # Moving percentile filter parameter, set 0.5 means median filter

'''USED IN VivaldiNeighborManager'''
VIVALDI_MAX_NEIGHBOR_NUM = 200
VIVALDI_SELECTED_NEIGHBOR_NUM = 32
VIVALDI_UPDATE_STRATEGY = 2 #0 means random, 1 means closest, 2 means hybrid
VIVALDI_UPLOAD_NUM = 2

'''USED IN PharosNCClient'''
PHAROS_USING_HEIGHT_GLOBAL = 1
PHAROS_USING_HEIGHT_LOCAL = 1
PHAROS_DIMENSION_GLOBAL = 4
PHAROS_DIMENSION_LOCAL = 2

'''USED IN PharosNeighborManager'''
PHAROS_UPDATE_STRATEGY_GLOBAL = 2
PHAROS_UPDATE_STRATEGY_LOCAL = 2
#PHAROS_USING_HEIGHT = VIVALDI_USING_HEIGHT
#PHAROS_GLOBAL_ERROR = 1.5
#PHAROS_GLOBAL_ERROR = 1.5

'''USED IN PHAROS BOOTSTRAP'''
PHAROS_LM = {"America":["planetlab-04.cs.princeton.edu","righthand.eecs.harvard.edu","planetlab04.cs.washington.edu","planetlab2.cs.ucla.edu","planetlab2.ucsd.edu","planetlab2.cs.duke.edu"], "Asia":["pl1.pku.edu.cn","csplanetlab2.kaist.ac.kr","planetlab-1.sjtu.edu.cn","planetlab3.ie.cuhk.edu.hk","planetlab2.netmedia.gist.ac.kr"], "Europe":["mars.planetlab.haw-hamburg.de","planetlab-3.imperial.ac.uk","planetlab1.tlm.unavarra.es","planetlab1.ceid.upatras.gr"] }  # lm and bootlist should have the same cluster ids
CLUSTER_BOOTLIST = {"America":["planetlab-04.cs.princeton.edu","righthand.eecs.harvard.edu","planetlab2.cs.ucla.edu","planetlab2.ucsd.edu","planetlab04.cs.washington.edu"], "Asia":["pl1.pku.edu.cn","csplanetlab2.kaist.ac.kr","planetlab-1.sjtu.edu.cn","node3.planet-lab.titech.ac.jp","planetlab2.netmedia.gist.ac.kr"], "Europe":["planetlab-3.imperial.ac.uk","planetlab1.tlm.unavarra.es","planetlab1.ceid.upatras.gr","planetlab2.informatik.uni-goettingen.de"] }
GLOBAL_BOOTLIST = ["planetlab2.netmedia.gist.ac.kr","pl1.pku.edu.cn","righthand.eecs.harvard.edu","pl2.planetlab.ics.tut.ac.jp","planetlab2.cs.ucla.edu","planetlab1.tlm.unavarra.es","planetlab-3.imperial.ac.uk","planetlab2.informatik.uni-goettingen.de","node3.planet-lab.titech.ac.jp"]

"""     pharos debug list nodes
planetlab2.informatik.uni-goettingen.de
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
planetlab04.cs.washington.edu
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
PHAROS_LOOP_TIME = 20  # make sure that PHAROS_LOOP_TIME>2*max(GOSSIPTIMEOUT,NCTIMEOUT,PINGTIMEOUT)

'''USED IN TWISTED'''
ALGORITHM = "PHAROS"
#ALGORITHM = "Vivaldi"
LOOPTIME = 10
PINGMETHOD = "UDP"
PINGPORT = 11230
PINGTIMEOUT = 3.0 #please ensure that PINGTIMEOUT<LOOPTIME and that it's a float
PINGNUM = 3
PINGBYTES = 56
GOSSIPPORT = 11238
NCPORT = 11239
GOSSIPTIMEOUT = 3 #please ensure that GOSSIPTIMEOUT<LOOPTIME
NCTIMEOUT = 3 #please ensure that NCTIMEOUT<LOOPTIME


'''INITIATE DEBUG MODE'''
DEBUG = False