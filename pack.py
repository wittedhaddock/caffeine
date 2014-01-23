# install a bunch of pack behavior on default objects

# This is somewhat clumsy because we cannot install methods on default types

import security


def findPackMethod(obj):
    if hasattr(obj, "_caffeinePack"):
        return obj.__class__._caffeinePack
    elif isinstance(obj, type):
        return typePack
    elif obj is None:
        return lambda x: {"_c": "NoneType"}  # we use a special sentinal value
    elif isinstance(obj, list):
        return listPack
    elif isinstance(obj, dict):
        return dictPack
    elif isinstance(obj, int):
        return lambda x: obj
    elif isinstance(obj, str):
        return lambda x: obj
    else:
        raise ValueError("Don't know how to pack %s" % obj.__class__)


def findUnpackMethod(packet):
        # Security warning: be careful when adding new methods here.  We assume
        # they're safe.
    if isinstance(packet, str):
        return lambda x: x

    print(packet, "packet was")
    klassname = packet["_c"]
    if klassname == "NoneType":
        return lambda x: None
    klass = security.string_to_class(klassname)
    if hasattr(klass, "_caffeineUnpack"):
        return klass._caffeineUnpack
    elif klassname == "dict":
        return dictUnpack
    elif klassname == "type":
        return typeUnpack
    else:
        raise ValueError("Don't know how to unpack %s" % klassname)


def pack(obj):
    method = findPackMethod(obj)
    return method(obj)


def unpack(packet):
    method = findUnpackMethod(packet)
    return method(packet)


def listPack(lyst):
    return {"_c": "list", "list": [pack(item) for item in lyst]}


def dictPack(dikt):
    return {"_c": "dict", "dict": {pack(key): pack(value) for key, value in dikt.items()}}


def dictUnpack(dikt):
    return {unpack(key): unpack(value) for key, value in dikt["dict"].items()}


def typePack(tipe):
    return {"_c": "type", "name": tipe.__name__}


def typeUnpack(tipe):
    return security.string_to_class(tipe["name"])
