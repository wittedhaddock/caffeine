"""This module does RPC stuff"""

root_level_objects = {}

import pack
import security

# This sweeps marked functions for RPC access.


def Class(klass):
    """A decorator used to mark that the class should be available over RPC"""
    root_level_objects[klass.__name__] = klass
    klass._caffeineRPC = {}
    for name, method in klass.__dict__.items():
        if hasattr(method, "_caffeineRPC"):
            klass._caffeineRPC[name] = method
    return klass

# We use a mark and sweep pattern.  The class doesn't exist at the time we
# create the function, so we just mark.  The sweep occurs in
# CaffeineClass.


def PublicMethod(method):
    """A decorator used to mark that the method should be available over RPC"""
    method._caffeineRPC = True
    return method


@Class
class Schema:
    """A schema contains type information for an arbitrary number of classes.  Most CaffeineService (e.g. a port) has one schema.
    You can get this schema by asking for CaffeineService.directory()."""

    def __init__(self, klass):
        self.klass = klass

    def _caffeinePack(self):
        """Pack the schema"""
        d = {}
        d["_c"] = "Schema"
        d["functions"] = {}
        for name, method in self.klass.__dict__.items():
            if hasattr(method, "_caffeineRPC"):
                annotations = dict(method.__func__.__annotations__)
                if "return" not in annotations:
                    annotations["return"] = None

                d["functions"][name] = pack.pack(annotations)
        return d

    @classmethod
    def _caffeineUnpack(klas, dykt):
        """Unpack the schema"""
        klass = security.string_to_class(dykt["_c"])
        newSchema = Schema(klass)
        newSchema.functions = {}
        for name,methodpack in dykt["functions"].items():
            newSchema.functions[name] = pack.unpack(methodpack)
        return newSchema

    def __repr__(self):
        return "<Schema for %s>" % self.klass


@Class
class CaffeineService:
    """Default object that provides caffeine services to a remote host"""

    @PublicMethod
    @classmethod
    def directory(self):
        """Returns the schema of objects supported by the remote host."""
        schemas = {}
        for name, object in root_level_objects.items():
            schemas[name] = Schema(object)
        return schemas
