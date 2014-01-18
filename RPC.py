root_level_objects = {}



# This sweeps marked functions for RPC access.
def Class(klass):
    root_level_objects[klass.__name__]=klass
    klass._caffeineRPC = {}
    for name,method in klass.__dict__.items():
        if hasattr(method,"_caffeineRPC"):
            klass._caffeineRPC[name] = method
    return klass

#We use a mark and sweep pattern.  The class doesn't exist at the time we create the function, so we just mark.  The sweep occurs in CaffeineClass.
def PublicMethod(method):
    method._caffeineRPC = True
    return method


class Schema:
    def __init__(self,klass):
        self.klass = klass

    def _caffeinePack(self):
        d = {}
        d["_c"]="Schema"
        d["functions"] = {}
        for name,method in self.klass.__dict__.items():
            if hasattr(method,"_caffeineRPC"):
                d["functions"][name] = method.__func__.__annotations__
        return d

    def __repr__(self):
        return "<Schema for %s>" % self.klass

@Class
class CaffeineService:
    @PublicMethod
    @classmethod
    def directory(self):
        schemas = {}
        for name,object in root_level_objects.items():
            schemas[name] = Schema(object)
        return schemas


