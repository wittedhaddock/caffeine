"""Verifies that the given selector is OK for remote use by the current user.  If it isn't okay, raises an exception."""

import RPC


class SecurityException(Exception):
    pass


def selector_is_ok(obj, selector):
    pass


def string_to_class(classname, root_level_objects=RPC.root_level_objects):
    real_directory = dict(root_level_objects, **{"dict":dict})
    return real_directory[classname]
