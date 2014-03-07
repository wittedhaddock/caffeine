#!python3
import caffeine.RPC
import caffeine.worker
import unittest
import sys


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    @unittest.skipUnless("test_loopback" in sys.argv, "You must explicitly enable test_loopback")
    def test_loopback(self):
        @caffeine.RPC.Class
        class Foo:

            @caffeine.RPC.PublicMethod
            @classmethod
            def hello_world(self) -> str:
                return "hello world"
        import subprocess
        import os
        self.router = subprocess.Popen(
            ["python3", os.path.join(caffeine.__path__[0], "../caffeine_router")], stdin=None, stdout=None, stderr=None)
        w = caffeine.worker.RPCWorker(root_objects={"Foo": Foo})
        w.runloop()
