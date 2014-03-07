import caffeine.RPC
import caffeine.worker


@caffeine.RPC.Class
class Foo:

    @caffeine.RPC.PublicMethod
    @classmethod
    def hello_world(self) -> str:
        return "hello world"

w = caffeine.worker.RPCWorker(root_objects={"Foo": Foo})
w.runloop()
