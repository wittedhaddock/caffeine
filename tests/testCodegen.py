#!python3
import caffeine.RPC
import unittest
import caffeine.codegen
import caffeine.worker


class TestSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_objc(self):

        @caffeine.RPC.Class
        class Foo:

            @caffeine.RPC.PublicMethod
            @classmethod
            def stringLength(self, string: str) -> int:
                return len(string)

        # spin up a worker that contains this class
        RPCWorker = caffeine.worker.RPCWorker({"Foo": Foo}, URL="inproc://test_objc")
        RPCWorker.start()

        class NotArgs:
            pass
        args = NotArgs()
        args.language = "objc"
        args.url = "inproc://test_objc"
        import tempfile
        args.output = tempfile.mkdtemp()
        caffeine.codegen.codegen(args)
        RPCWorker.stop()

    def testUnderscoreCaseToCamelCase(self):
        self.assertEqual(caffeine.codegen.ObjCCodeGen(schemas=[],args=[]).underscore_case_to_camel_case("hello_world"),"helloWorld")

    def testMultiplatformEmit(self):
        @caffeine.RPC.Class
        class Foo:

            @caffeine.RPC.PublicMethod
            @classmethod
            def hello_world(self) -> str:
                return "hello world"

        # spin up a worker that contains this class
        RPCWorker = caffeine.worker.RPCWorker({"Foo": Foo}, URL="inproc://test_objc")
        RPCWorker.start()
        import tempfile

        class NotArgs:
            pass
        args = NotArgs()
        args.language = "objc"
        args.url = "inproc://test_objc"
        args.output = tempfile.mkdtemp()
        print(caffeine.codegen.codegen(args))
        import os.path
        print ("Generated to %s" % args.output)
        self.assertTrue(os.path.exists(args.output + "/Foo.m"))
        self.assertTrue(os.path.exists(args.output + "/Foo.h"))
        self.assertTrue(os.path.exists(args.output + "/CaffeineService.m"))
        self.assertTrue(os.path.exists(args.output + "/CaffeineService.h"))

        with open(args.output + "/Foo.h") as implementation:
            implementation = implementation.read()
            self.assertTrue("+ (NSString*)helloWorldWithError:(NSError**)error" in implementation)

        #let's see if the generated code compiles
        #At this precise moment we can't introduce a dependency on CaffeineClient.h
        #This could be revisited in the future
        #import subprocess
        #subprocess.check_call(["clang","-c",args.output+"/Foo.m"])

        RPCWorker.stop()
