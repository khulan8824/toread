#!/usr/bin/bash
# usage: sh compareServer.sh servers.txt myPLnodes.txt
#	read the content of servers.txt line by line and check weather the host is in the file myPLnodes.txt, print out the hosts which are in the server.txt but not in myPLnodes.txt
if [ $# -ne 2 ]
then
	echo "Give two arguments!"
	echo "usage: sh compareServer.sh servers.txt myPLnodes.txt"
	exit 1
fi

cat $1 | while read line
do
#	echo $line
	expr index "#" "$line">/dev/null
	#echo "index  ",$?
	if [ $? -ne 0 ]
	then
		#grep $line $2>/dev/null
		#echo "grep $line $2        result:" $?
		grep $line $2>/dev/null
		if [ $? -ne 0 ]
		then
			echo "$line"
		fi
	fi
done
