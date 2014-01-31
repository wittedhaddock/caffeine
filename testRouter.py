
import unittest


class TestSequence(unittest.TestCase):

    def setUp(self):
        # we start the router
        import sys
        sys.path.append("..")
        import caffeine
        import subprocess
        import os.path
        print("Everything started OK?")

        self.router = subprocess.Popen(
            ["python3", os.path.join(caffeine.__path__[0], "router.py")], stdin=None, stdout=None, stderr=None)

        self.worker = subprocess.Popen(
            ["python3", os.path.join(caffeine.__path__[0], "testRouterWorkerProcess.py")], stdin=None, stdout=None, stderr=None)

    def test_rountrip(self):
        import zmq
        import sys
        sys.path.append("..")
        import caffeine
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        client_public, client_secret = zmq.curve_keypair()
        socket.curve_publickey = client_public
        socket.curve_secretkey = client_secret
        socket.curve_serverkey = caffeine.well_known_public_key
        socket.connect("tcp://localhost:55555")
        socket.send_multipart([b'test1'])
        msg = socket.recv_multipart()
        print(msg)
        self.assertEquals(msg[1], b"worker says hello")

    def tearDown(self):
        self.router.kill()
        self.worker.kill()
