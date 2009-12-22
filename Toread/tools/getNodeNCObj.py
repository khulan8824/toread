import socket
from config import *
import pickle

PORT=NCPORT
BUFLEN = 2048

def getNC( hostname, token ):
	sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ip = socket.gethostbyname(hostname)
	sockfd.settimeout(10)
	try:
		sockfd.connect((ip,PORT))
		sockfd.send(token)
		ncbuf = sockfd.recv(BUFLEN)
		sockfd.close()
		#print "received data length:",len(ncbuf)
		ncobj = pickle.loads(ncbuf)
		return ncobj
	except Exception,e:
		print "Error when connecting to ", hostname,":",PORT
		print "Exception msg:",e
		sockfd.close()
		return None
#		sys.exit(1)
