FROM stackbrew/debian:7.3
MAINTAINER drew

#update debian
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install pkg-config -y

#install curl
RUN apt-get install curl -y

#install build tools
RUN apt-get install build-essential -y

#install python
RUN apt-get install libssl-dev -y #we need OpenSSL for distribute installation
RUN curl -o python.tgz http://www.python.org/ftp/python/3.3.3/Python-3.3.3.tgz
RUN tar xf python.tgz
RUN cd Python-3.3.3 && ./configure
RUN cd Python-3.3.3 && make
RUN cd Python-3.3.3 && make install

#setup distribute
RUN curl -O http://python-distribute.org/distribute_setup.py
RUN python3.3 distribute_setup.py
RUN python3.3 -m easy_install pip


#install pyzmq
#first, let's get libsodium
RUN curl -O http://download.libsodium.org/libsodium/releases/libsodium-0.4.5.tar.gz
RUN tar xf libsodium-0.4.5.tar.gz
RUN cd libsodium-0.4.5 && ./configure
RUN cd libsodium-0.4.5 && make
RUN cd libsodium-0.4.5 && make install
RUN ldconfig
#now, let's get particular libzmq
RUN curl -O http://download.zeromq.org/zeromq-4.0.3.tar.gz
RUN tar xf zeromq-4.0.3.tar.gz
RUN cd zeromq-4.0.3 && ./configure
RUN cd zeromq-4.0.3 && make
RUN cd zeromq-4.0.3 && make install
RUN ldconfig
#now install the python binding
RUN pip-3.3 install pyzmq

#install supervisord
RUN apt-get install -y supervisord

#install teamcity-messages
RUN pip-3.3 install teamcity-messages

#run router
ADD * .
EXPOSE 55555 55555

ENTRYPOINT python3.3 router.py
