#©2013 Drew Crawford Apps.  All Rights Reserved.
#See LICENSE file for details.

import zmq
import sys
sys.path.append(sys.path[0]+"/..")
import caffeine
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(caffeine.internal_url)
socket.send(b'_READY')
print("sent ready")
while True:
	message = socket.recv_multipart()
	print("worker saying hello",message)
	socket.send_multipart([message[0],b'worker says hello'])
