sleep 120m
ps aux  |  grep -i main.py  |  awk '{print $2}'  | sudo xargs kill -9