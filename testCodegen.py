#!python3
import RPC
import unittest
import worker


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_ObjC(self):

        @RPC.Class
        class Foo:

            @RPC.PublicMethod
            @classmethod
            def stringLength(self, string: str) -> int:
                return len(string)

        # spin up a client
        client = worker.RPCClient(URL="tcp://127.0.0.1:12345")

        # spin up a worker that contains this class
        RPCWorker = worker.RPCWorker({"Foo": Foo}, URL="tcp://127.0.0.1:12345")
        RPCWorker.start()

        serviceObject = client.CaffeineService
        print(serviceObject.directory(), "directory")
        RPCWorker.stop()
