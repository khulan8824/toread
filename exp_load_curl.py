
from time import time,sleep
from subprocess import check_output, PIPE, Popen
import csv
import simpleflock
import shlex
import os
import string
import random

NUM=''

EXP_TIME = 15*60
FILE = "load_exp_ttfb"
VIV_FILE = "vivaldi_ttfb"
EXP_FILE = "my_proxy"
USER = 'david.pinilla'
PASS = r'|Jn 5DJ\\7inbNniK|m@^ja&>C'

PROXY = "10.228.0.83"

URL = "www.google.com"

def get_cmd2(proxy=PROXY):
	hash = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(50))
	url = URL+'/'+hash
        cmd='curl -x '+proxy+':3128 -U '+USER+':\"'+PASS+'\" -m 180 -w %{time_starttransfer} '+url+' -o /dev/null -s'
        #cmd='curl -x '+proxy+':3128 -U '+USER+':\"'+PASS+'\" -m 180 -w %{time_starttransfer} '+url+' -s'
        return cmd

def getVivaldiProxy():
	with simpleflock.SimpleFlock('/tmp/foolock1'):
		with open('proxy_route_table','r') as f:
			global PROXY
   			r = csv.reader(f,delimiter='\t')
			new_proxy = None
			for row in r:
				if row[5] == 'True':
					new_proxy = row[0]
					break
			if new_proxy != PROXY:
				ema025 = EMA(0.25)
				temp_ema025 = EMA(0.25)
				ema005 = EMA(0.05)
				temp_ema005 = EMA(0.05)
				ema075 = EMA(0.75)
				temp_ema075 = EMA(0.75)
			PROXY = new_proxy

def getVivaldiDistance(proxy):
	result = 0.0
	with simpleflock.SimpleFlock('/tmp/foolock1'):
		with open('proxy_route_table','r') as f:
    			r = csv.reader(f,delimiter='\t')
			for row in r:
        			if row[0]==proxy:
					result = float(row[1])/1000
	return result

class EMA(object):

    def __init__(self, a):
        self.a = a
        self.last = 0
	self.count = 0	

    def compute(self, value):
        #data is list of ordered value wich is already clean and numerical
        if  self.count == 0 :
            self.last = float(value)
        else:
            self.last = self.a *float(value) + (1-self.a)*float(self.last)

        self.count = self.count+1
        return self.last

with open(FILE,"wb") as f:
	f.write("time,TTFB"+num+",TTFB_ema_0.25"+num+",TTFB_temp_ema_0.25"+num+",TTFB_ema_0.05"+num+",TTFB_temp_ema_0.05"+num+",TTFB_ema_0.75"+num+",TTFB_temp_ema_0.75"+num+",type"+num+",vivaldi_time"+num+"\n")
#print("time,TTFB,TTFB_ema_0.25,TTFB_temp_ema_0.25,TTFB_ema_0.5,TTFB_temp_ema_0.5,TTFB_ema_0.75,TTFB_temp_ema_0.75,type,vivaldi_time\n")
with open(EXP_FILE,"wb") as f:
	f.write('time,proxy\n')
VIVALDI_PERIOD = 10
last_vivaldi = 0
t=0
START = time()
for i in range(0,15):
	sleep(1);
	t = time() - START
	with open(FILE,'wb') as f:
		f.write("{0:.1f},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(t,0,0,0,0,0,0,0,'est',0))
	with open(EXP_FILE,'wb') as f:
		f.write("{0:.1f},{1}\n".format(t,'None'))

getVivaldiProxy()
vivaldi_time = getVivaldiDistance(PROXY)

command = Popen(shlex.split(get_cmd2(PROXY)),stdout=PIPE, stderr=PIPE)
last_value = 0
type = 'meas'
last_time = START
out = 0


ema025 = EMA(0.25)
temp_ema025 = EMA(0.25)
ema005 = EMA(0.05)
temp_ema005 = EMA(0.05)
ema075 = EMA(0.75)
temp_ema075 = EMA(0.75)


while t < (EXP_TIME+60):
	sleep(0.9945)
	code = command.poll()
	if code is not None:
		if code==0 :
			out, err = command.communicate()
			type = 'meas'
		final_out = float(out)-vivaldi_time
		last_value = final_out
		last_time = time()
		command = Popen(shlex.split(get_cmd2(PROXY)),stdout=PIPE, stderr=PIPE)
		ema025.compute(final_out)
		temp_ema025.last = ema025.last
		ema005.compute(final_out)
		temp_ema005.last = ema005.last
		ema075.compute(final_out)
		temp_ema075.last = ema075.last
	else:	
		temp_time = time()
		if (temp_time-last_time)>last_value:
			last_value = temp_time-last_time 
		#out = last_value
		temp_ema025.compute(float(last_value))
		temp_ema005.compute(float(last_value))
		temp_ema075.compute(float(last_value))
		type = 'est'
		
	t = time()-START
	if (t-last_vivaldi) > VIVALDI_PERIOD:
		vivaldi_time = getVivaldiDistance(PROXY)
		last_vivaldi = t
	with open(FILE,'a') as f:
		f.write("{0:.1f},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(t,out,ema025.last,temp_ema025.last,ema005.last,temp_ema005.last,ema075.last,temp_ema075.last,type,vivaldi_time))
	with open(EXP_FILE,'a') as f:
		f.write("{0:.1f},{1}\n".format(t,PROXY))
	with simpleflock.SimpleFlock('/tmp/foolock'):
		with open(VIV_FILE,'a') as viv:
			viv.write("{},{}\n".format(PROXY,temp_ema005.last))
	getVivaldiProxy()
	#print("{0:.1f},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(t,out,ema025.last,temp_ema025.last,ema005.last,temp_ema005.last,ema075.last,temp_ema075.last,type,vivaldi_time))

