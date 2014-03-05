#!python3
import RPC
import unittest


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_loopback(self):
        @RPC.Class
        class Foo:
            @RPC.PublicMethod
            @classmethod
            def hello_world(self) -> str:
                return "hello world"
        import subprocess
        import os
        import import_caffeine
        import caffeine
        self.router = subprocess.Popen(
            ["python3", os.path.join(caffeine.__path__[0], "router.py")], stdin=None, stdout=None, stderr=None)
        from worker import RPCWorker
        w = RPCWorker(root_objects={"Foo":Foo})
        w.runloop()
