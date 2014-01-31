#!python3
import RPC
import unittest
import codegen
import worker


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_objc(self):

        @RPC.Class
        class Foo:

            @RPC.PublicMethod
            @classmethod
            def stringLength(self, string: str) -> int:
                return len(string)

        # spin up a worker that contains this class
        RPCWorker = worker.RPCWorker({"Foo": Foo}, URL="inproc://test_objc")
        RPCWorker.start()

        class NotArgs:
            pass
        args = NotArgs()
        args.language = "objc"
        args.url = "inproc://test_objc"
        codegen.codegen(args)
        RPCWorker.stop()
