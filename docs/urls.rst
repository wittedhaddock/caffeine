URLs
=====

Caffeine URLs take the form

scheme://user:pass@host:port?skey

where

* scheme is currently tcp
* user is a public caffeine :term:`key`
* pass is a private caffeine :term:`key`
* server is the public caffeine :term:`key` of the server.  There is no key exchange mechanism; the server's key must be known.

A caffeine key generally appears in one of two forms.  It can be expressed as an array of bytes, e.g. [0x01, 0x03, 0xFF...]

When used in a URL, however, the key is expressed as the `Y64 <http://www.yuiblog.com/blog/2010/07/06/in-the-yui-3-gallery-base64-and-y64-encoding/>`_ encoding of that array of bytes.    