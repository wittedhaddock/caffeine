import RPC
import unittest


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_decorate(self):
        @RPC.Class
        class Foo:

            @RPC.PublicMethod
            @classmethod
            def helloWorld(self):
                return "hello world"
        self.assertEquals(Foo.helloWorld(), "hello world")
        self.assertEquals(
            Foo._caffeineRPC["helloWorld"].__func__, Foo.helloWorld.__func__)
        self.assertEquals(RPC.root_level_objects["Foo"], Foo)

    def test_schema(self):
        @RPC.Class
        class Foo:

            @RPC.PublicMethod
            @classmethod
            def stringLength(self, string: str) -> int:
                return len(string)

        args = []
        kwargs = {"string": "Test1"}
        print("length is ", Foo.stringLength(*args, **kwargs))

        print(RPC.Schema(Foo)._caffeinePack())
        directory = RPC.CaffeineService.directory()
        fooPackedSchema = directory["Foo"]._caffeinePack()
        self.assertTrue(fooPackedSchema["functions"])

    def test_RPCCall(self):
        import worker
        import pack
        @RPC.Class
        class Foo:

            @RPC.PublicMethod
            @classmethod
            def stringLength(self, string: str) -> int:
                return len(string)

        RPCWorker = worker.RPCWorker({"Foo": Foo})
        kwargs = {"string":"test123"}
        packed_kwargs = pack.pack(kwargs)
        RPCWorker.handleMessage({"_c": "Foo", "_s": "stringLength", "_a": packed_kwargs})

