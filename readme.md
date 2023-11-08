#win
docker run -ti --name=bz -p 8990:8990 -v E:\py-project\bz:/home/bz --net=server_myserver_v1 allonvendia/ufo:v1.0
#linux
docker run -ti --name= -v /home/server/www/py-jav:/home/jav -p 8992:8992 --link myredis --link mydb --network= allonvendia/ufo:v1.0 /bin/sh
#mitmproxy
nohup mitmproxy -s mitm.py > mitmproxy.log 2>&1 &