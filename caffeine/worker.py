#!python3
#©2013 Drew Crawford Apps.  All Rights Reserved.
# See LICENSE file for details.

import caffeine.pack
import caffeine
import zmq
import umsgpack
import caffeine.security as security

Context = None


def get_context():
    global Context
    if Context:
        return Context
    Context = zmq.Context()
    return Context


# A base worker class.  Primarily used for plubming.


class Worker:

    def __init__(self, URL=caffeine.internal_url):
        self.url = URL
        self.should_stop = False
        pass

    # override this method in subclasses
    def handle_message(self, msg):
        pass

    def runloop(self):
        context = get_context()
        socket = context.socket(zmq.REQ)
        socket.connect(self.url)
        import time
        time.sleep(2)
        socket.send(b'_READY')
        print("sent ready on URL %s" % self.url)
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        while not self.should_stop:
            socks = dict(poller.poll(timeout=500))
            if socket in socks and socks[socket] == zmq.POLLIN:
                message = socket.recv_multipart()
                # so there are two cases here.  Either the message is of length 3, which is a router-type packet.  In this case we preserve the header. The header exists to help the router identify where the packet should ultimately go.
                # or, the message is of length 1, which is a direct connection.
                header = None

                if len(message) == 3:
                    header = message[0]
                    message = message[2]
                elif len(message) == 1:
                    message = message[0]
                else:
                    raise ValueError("Unknown message format %s" % message)
                response = self.handle_message(message)
                print("response", response)
                if header:
                    print("worker sending %s" % [header, b'', response])
                    socket.send_multipart([header, response])
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
        import caffeine.RPC as RPC
        # extend CaffeineServiceObject for availability over RPC
        self.root_objects["CaffeineService"] = RPC.CaffeineService
        super().__init__(URL=URL)

    def handle_message(self, msg):
        msg = umsgpack.loads(msg)
        if msg["_c"] not in self.root_objects:
            raise security.SecurityException(
                "Class %s is not available to RPC worker %s, so you cannot send messages to it." % (msg["_c"], self))
        obj = self.root_objects[msg["_c"]]
        selector = msg["_s"]
        security.selector_is_ok(obj, selector)
        method = getattr(obj, selector)
        kwargs = caffeine.pack.unpack(msg["_a"])
        result = method(**kwargs)
        print("result is", result)
        dictFormat = caffeine.pack.pack(result)
        print("dict is", dictFormat)
        return umsgpack.dumps(dictFormat)


class RPCClient():

    def __init__(self, url):
        context = get_context()
        import caffeine.keytools
        (zeromq_url, z85_public, z85_private,
         z85_server) = caffeine.keytools.parseURL(url)
        
        if z85_server:
            #In this case, we enable encryption and assume we're talking to a ROUTER
            self.socket = context.socket(zmq.REQ)
            client_public, client_secret = zmq.curve_keypair()
            self.socket.curve_publickey = z85_public
            self.socket.curve_secretkey = z85_private
            self.socket.curve_serverkey = z85_server
            self.burned_ready = True #not required for router
            self.router_style_messages = True
            self.socket.connect(zeromq_url)

        else:
            #In this case, we handle direct mode
            self.burned_ready = False
            self.socket = context.socket(zmq.REP)
            self.router_style_messages = False
            self.socket.bind(zeromq_url)

        print (zeromq_url,z85_public,z85_private,z85_server)
        print("client connecting to URL %s" % url)

    def __getattr__(self, name):
        class ClassProxy:

            def __init__(self, client, class_name):
                self.client = client
                self.class_name = class_name

            def __getattr__(self, name):
                class FunctionProxy:

                    def __init__(self, client, class_name, method_name):
                        self.client = client
                        self.class_name = class_name
                        self.method_name = method_name

                    def __call__(self, *args, **kwargs):
                        if not self.client.burned_ready:
                            self.client.burned_ready = True
                            self.client.socket.recv_multipart()

                        packedObj = {
                            "_c": self.class_name, "_s": self.method_name, "_a": caffeine.pack.pack(kwargs)}
                        packedBytes = umsgpack.dumps(packedObj)

                        result = self.client.socket.send(packedBytes)

                        result = self.client.socket.recv_multipart()
                        if self.client.router_style_messages:
                            result = result[1]
                        else:
                            result = result[0]
                        return caffeine.pack.unpack(umsgpack.loads(result))
                return FunctionProxy(object.__getattribute__(self, "client"), object.__getattribute__(self, "class_name"), name)

        return ClassProxy(self, name)

        """
        socket.send_multipart([b'test1',b'test2'])
        msg = socket.recv_multipart()
        print (msg)
        self.assertEquals(msg[1],b"worker says hello") """
