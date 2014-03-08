Wire format
=============

This document describes the caffeine wire format.  You would use this to understand the network stack implementation.

zeroMQ
########

At present caffeine uses `zeroMQ <http://zeromq.org>`_ with its `CurveZMQ <http://rfc.zeromq.org/spec:26>`_ extension.  :doc:`urls` are decoded into CurveZMQ parameters.

.. _serialization:

MsgPack
########

Caffeine serializes object graphs using the `MsgPack "v2" specification <https://github.com/msgpack/msgpack/blob/master/spec.md>`_.  You must be careful with MsgPack; not all implementations are compatible, and the difference is important.

.. _rpc_wire:

RPC Wire Format.
#####

Class methods (e.g. static methods)
++++++++++++++++++++++++++++++++++++

To invoke a static method, send:

* ``_c``: the name of the class
* ``_s``: the name of the method
* ``_a``: The arguments.  Caffeine accepts only keyword arguments as a dictionary.

Errata
++++++++

An error type (e.g. ``NSError``, ``Exception``, etc.) is not generally acceptable for a return type.  Returning an NSError/Exception is equivalent to claiming that the exception was thrown during the method invocation.

The argument ``return`` is reserved.  "return" is a reserved word in many languages so it is unlikely you will try to use it, but in languages where it might be legal, no caffeine method can have an argument called "return".

Types that begin with "_" are reserved.  You cannot have a type called ``_int``, for example.

