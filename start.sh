#!/bin/bash
#docker run -ti --name= -v /home/server/www/py-jav:/home/jav -p 8992:8992 --link myredis --link mydb --network= allonvendia/ufo:v1.0 /bin/sh
python3 main.py > output.log 2>&1 &