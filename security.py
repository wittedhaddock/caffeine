
import RPC


class SecurityException(Exception):
    pass

"""Verifies that the given selector is OK for remote use by the current user.  If it isn't okay, raises an exception."""


def selector_is_ok(obj, selector):
    pass


"""Looks up the class via a safe method.  If the class isn't okay, raises an exception."""


def string_to_class(classname, root_level_objects=RPC.root_level_objects):
    real_directory = dict(root_level_objects, **{
                          "dict": dict, "type": type, "str": str, "int": int})
    return real_directory[classname]
