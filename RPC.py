root_level_objects = {}

def CaffeineClass(klass):
    root_level_objects[klass.__name__]=klass
    klass._caffeineRPC = {}
    for name,method in klass.__dict__.items():
        if hasattr(method,"_caffeineRPC"):
            klass._caffeineRPC[name] = method
    return klass

def CaffeinePublicMethod(method):
    method._caffeineRPC = True
    return method


