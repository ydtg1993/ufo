#docker 
#win
`docker run -ti --name=bz -p 8990:8990 -v E:\py-project\bz:/home/bz --net=server_myserver_v1 allonvendia/ufo:v1.0`
#linux
`docker run -ti --name= -v /home/server/www/py-jav:/home/jav -p 8992:8992 --link myredis --link mydb --network= allonvendia/ufo:v1.0 /bin/sh`

#mitmproxy
    echo "nameserver 8.8.8.8" > /etc/resolv.conf
    wget https://sh.rustup.rs -O rustup-init.sh
    sh rustup-init.sh
    source $HOME/.cargo/env
    apk add openssl ca-certificates  linux-headers libffi-dev libressl zlib zlib-dev 
    apk add bsd-compat-headers
    pip3 install mitmproxy
    
#install ssl certificate
`mitmdump`
`cp ~/.mitmproxy/mitmproxy-ca-cert.pem /etc/ssl/certs/mitmproxy.crt`
`update-ca-certificates`

`apk add nss-tools`
`mkdir -p $HOME/.pki/nssdb`
`certutil -d sql:$HOME/.pki/nssdb -N`
`certutil -d sql:$HOME/.pki/nssdb -A -t "C,," -n mitmproxy -i /etc/ssl/certs/ca-certificates.crt`
`certutil -d sql:$HOME/.pki/nssdb -L`

#mitmproxy
#win
`mitmdump.exe -s mitm.py > mitmproxy.log &`
#linux
`mitmdump -p 8080 -s mitm.py > mitmproxy.log 2>&1 &`