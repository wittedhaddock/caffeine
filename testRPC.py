import RPC
import unittest
class TestSequence(unittest.TestCase):
    def setUp(self):
    	pass
    def test_decorate(self):
    	@RPC.CaffeineClass
    	class Foo:
    		@RPC.CaffeinePublicMethod
    		@classmethod
    		def helloWorld(self):
    			return "hello world"
    	self.assertEquals(Foo.helloWorld(),"hello world")
    	self.assertEquals(Foo._caffeineRPC["helloWorld"].__func__,Foo.helloWorld.__func__)
    	self.assertEquals(RPC.root_level_objects["Foo"],Foo)

    def test_schema(self):
    	@RPC.CaffeineClass
    	class Foo:
    		@RPC.CaffeinePublicMethod
    		@classmethod
    		def stringLength(self,string:str) -> int:
    			return len(string)

    	args = []
    	kwargs = {"string":"Test1"}
    	print ("length is ",Foo.stringLength(*args,**kwargs))

    	print (RPC.Schema(Foo)._caffeinePack())
    	directory = RPC.CaffeineService.directory()
    	fooPackedSchema = directory["Foo"]._caffeinePack()
    	self.assertTrue(fooPackedSchema["functions"])




