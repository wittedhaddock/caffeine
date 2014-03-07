import caffeine.RPC
import unittest


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_decorate(self):
        @caffeine.RPC.Class
        class Foo:

            @caffeine.RPC.PublicMethod
            @classmethod
            def helloWorld(self):
                return "hello world"
        self.assertEquals(Foo.helloWorld(), "hello world")
        self.assertEquals(
            Foo._caffeineRPC["helloWorld"].__func__, Foo.helloWorld.__func__)
        self.assertEquals(caffeine.RPC.root_level_objects["Foo"], Foo)

    def test_schema(self):
        @caffeine.RPC.Class
        class Foo:

            @caffeine.RPC.PublicMethod
            @classmethod
            def stringLength(self, string: str) -> int:
                return len(string)

        args = []
        kwargs = {"string": "Test1"}
        print("length is ", Foo.stringLength(*args, **kwargs))

        print(caffeine.RPC.Schema(Foo)._caffeinePack())
        directory = caffeine.RPC.CaffeineService.directory()
        fooPackedSchema = directory["Foo"]._caffeinePack()
        self.assertTrue(fooPackedSchema["functions"])

    def test_RPCCall(self):
        import caffeine.worker
        import caffeine.pack

        @caffeine.RPC.Class
        class Foo:

            @caffeine.RPC.PublicMethod
            @classmethod
            def stringLength(self, string: str) -> int:
                return len(string)

        RPCWorker = caffeine.worker.RPCWorker({"Foo": Foo})
        kwargs = {"string": "test123"}
        packed_kwargs = caffeine.pack.pack(kwargs)
        import umsgpack
        RPCWorker.handle_message(
            umsgpack.dumps({"_c": "Foo", "_s": "stringLength", "_a": packed_kwargs}))
