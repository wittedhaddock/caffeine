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

