#©2013 Drew Crawford Apps.  All Rights Reserved.
#See LICENSE file for details.

import zmq
import sys
sys.path.append(sys.path[0]+"/..")
print(sys.path)

import caffeine
context = zmq.Context()


def zap_handler():
	#see http://rfc.zeromq.org/spec:27
	socket = context.socket(zmq.REP)
	socket.bind("inproc://zeromq.zap.01")
	while True:
		msg = socket.recv_multipart()
		print ("ZAP",msg)
		version, sequence, domain, address, identity, mechanism, publickey = msg[:7]
		assert version==b"1.0"
		assert mechanism==b"CURVE"
		#although the spec specifies a blank packet here, apparrently one is not desired.  Sort of a mystery.
		socket.send_multipart([b"1.0",sequence,b"200",b"OK",b"Jeff",b""])
		#I've written the mailing list for help associating a client with a server.


frontend_socket = context.socket(zmq.ROUTER)
(public,private) = zmq.curve_keypair()
frontend_socket.curve_serverkey = caffeine.well_known_public_key
frontend_socket.curve_secretkey = caffeine.well_known_private_key
frontend_socket.curve_server = True
frontend_socket.bind("tcp://127.0.0.1:%d" % caffeine.client_port)

backend_socket = context.socket(zmq.ROUTER)
backend_socket.bind(caffeine.internal_url)
print("Router serving to workers on URI ",caffeine.internal_url)


print ("Router fielding requests on port",caffeine.client_port)

#http://zguide.zeromq.org/py:lbbroker2

poller = zmq.Poller()
# Always poll for worker activity on backend
poller.register(backend_socket, zmq.POLLIN)

# Poll front-end only if we have available workers
poller.register(frontend_socket, zmq.POLLIN)

from threading import Thread
zap_thread = Thread(target=zap_handler)
zap_thread.start()
available_workers = 0
workers = []

while True:
	socks = dict(poller.poll())
	print(socks)
	print("those were the socks")
	if (backend_socket in socks and socks[backend_socket]==zmq.POLLIN):
		print("c1")
		message = backend_socket.recv_multipart()
		print (message)
		worker_addr = message[0]
		assert available_workers < caffeine.number_of_worker_processes
		available_workers += 1
		workers.append(worker_addr)
		empty = message[1]
		assert empty == b""
		client_addr = message[2]
		if client_addr != b"_READY":
			reply = message[2:]
			frontend_socket.send_multipart([client_addr,b""] + reply)
			print ("sent",[client_addr,b""] + reply)
	if available_workers > 0:
		print("c2")
		if (frontend_socket in socks and socks[frontend_socket]==zmq.POLLIN):
			message = frontend_socket.recv_multipart()
			client_addr = message[0]
			empty = message[1]
			assert empty==b""
			available_workers -= 1
			worker_addr = workers.pop()
			backend_socket.send_multipart([worker_addr, b"", client_addr, b""] + message[2:])
import time
time.sleep(1)
frontend_socket.close()
backend_socket.close()
context.term()


