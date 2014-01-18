#©2013 Drew Crawford Apps.  All Rights Reserved.
#See LICENSE file for details.


class Worker:
	def __init__(self):
		pass

	#override this method in subclasses
	def handleMessage(self,msg):
		pass
	def runloop(self):

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
			socket.send_multipart([message[0],self.handleMessage(message[1:])])

