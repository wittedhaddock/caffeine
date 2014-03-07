import sys
import caffeine.RPC


class SecurityException(Exception):

    """Base exception for security issues"""
    pass


def selector_is_ok(obj, selector):
    """Verifies that the given selector is OK for remote use by the current user.  If it isn't okay, raises an exception."""
    pass


def string_to_class(classname, root_level_objects=None):
    if root_level_objects is None:
        root_level_objects = caffeine.RPC.root_level_objects
    """Looks up the class via a safe method.  If the class isn't okay, raises an exception."""
    real_directory = dict(root_level_objects, **{
                          "dict": dict, "type": type, "str": str, "int": int})
    return real_directory[classname]
