#!python3
#©2013 Drew Crawford Apps.  All Rights Reserved.
# See LICENSE file for details.

import pack
import import_caffeine
import caffeine
import zmq
import umsgpack
import security

context = None


def getContext():
    global context
    if context:
        return context
    context = zmq.Context()
    return context


# A base worker class.  Primarily used for plubming.


class Worker:

    def __init__(self, URL=caffeine.internal_url):
        self.url = URL
        self.should_stop = False
        pass

    # override this method in subclasses
    def handleMessage(self, msg):
        pass

    def runloop(self):
        context = getContext()
        socket = context.socket(zmq.REQ)
        socket.connect(self.url)
        import time
        time.sleep(2)
        socket.send(b'_READY')
        print("sent ready on URL %s" % self.url)
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        while not self.should_stop:
            print ("got here")
            socks = dict(poller.poll(timeout=500))
            if socket in socks and socks[socket]==zmq.POLLIN:
                message = socket.recv_multipart()
                #so there are two cases here.  Either the message is of length 3, which is a router-type packet.  In this case we preserve the header. The header exists to help the router identify where the packet should ultimately go. 
                #or, the message is of length 1, which is a direct connection.
                header = None

                if len(message)==3:
                    header = message[0]
                    message = message[2]
                elif len(message)==1:
                    message = message[0]
                else:
                    raise ValueError("Unknown message format %s" % message)
                response = self.handleMessage(message)
                print("response",response)
                if header:
                    print ("worker sending %s" % [header,b'',response])
                    socket.send_multipart([header,response])
                else:
                    socket.send_multipart([response])

    def start(self):
        import threading
        self.thread = threading.Thread(target=self.runloop)
        self.should_stop = False
        self.thread.start()

    def stop(self):
        self.should_stop = True

"""This class handles typical caffeine RPC requests"""


class RPCWorker(Worker):

    def __init__(self, root_objects, URL=caffeine.internal_url):
        self.root_objects = root_objects
        import RPC
        self.root_objects["CaffeineService"] = RPC.CaffeineService #extend CaffeineServiceObject for availability over RPC
        super().__init__(URL=URL)

    def handleMessage(self, msg):
        msg = umsgpack.loads(msg)
        if msg["_c"] not in self.root_objects:
            raise security.SecurityException("Class %s is not available to RPC worker %s, so you cannot send messages to it." % (msg["_c"],self))
        obj = self.root_objects[msg["_c"]]
        selector = msg["_s"]
        security.selector_is_ok(obj, selector)
        method = getattr(obj, selector)
        kwargs = pack.unpack(msg["_a"])
        result = method(**kwargs)
        print ("result is",result)
        dictFormat = pack.pack(result)
        print ("dict is",dictFormat)
        return umsgpack.dumps(dictFormat)


class RPCClient():

    def __init__(self, URL):
        context = getContext()
        self.socket = context.socket(zmq.REP)
        print("client connecting to URL %s" % URL)
        self.socket.bind(URL)
        self.burned_ready = False


    def __getattr__(self, name):
        class ClassProxy:

            def __init__(self, client, className):
                self.client = client
                self.className = className

            def __getattr__(self, name):
                class FunctionProxy:

                    def __init__(self, client, className, methodName):
                        self.client = client
                        self.className = className
                        self.methodName = methodName

                    def __call__(self, *args, **kwargs):
                        if not self.client.burned_ready:
                            self.client.burned_ready = True
                            self.client.socket.recv_multipart()

                        packedObj = {
                            "_c": self.className, "_s": self.methodName, "_a": pack.pack(kwargs)}
                        packedBytes = umsgpack.dumps(packedObj)

                        result = self.client.socket.send(packedBytes)
                        result = self.client.socket.recv_multipart()[0]
                        return pack.unpack(umsgpack.loads(result))
                return FunctionProxy(object.__getattribute__(self, "client"), object.__getattribute__(self, "className"), name)

        return ClassProxy(self, name)

        """
        socket.send_multipart([b'test1',b'test2'])
        msg = socket.recv_multipart()
        print (msg)
        self.assertEquals(msg[1],b"worker says hello") """
