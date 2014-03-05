# URIs

Caffeine URIs take the form

scheme://user:pass@host:port?skey

where

* scheme is currently tcp
* user is a public caffeine key
* pass is a private caffeine key
* server is the public caffeine key of the server.  There is no key exchange mechanism; the server's key must be known.

A caffeine key generally appears in one of two forms.  It can be expressed as an array of bytes, e.g. [0x01, 0x03, 0xFF...]

When used in a URL, however, the key is expressed as the [Y64](http://www.yuiblog.com/blog/2010/07/06/in-the-yui-3-gallery-base64-and-y64-encoding/) encoding of that array of bytes.    

# Wire format

A wire format specification

## RPC

### Errata

An error type (e.g. NSError, Exception, etc.) is not generally acceptable for a return type.  Returning an NSError/Exception is equivalent to claiming that the exception was thrown during the method invocation.

The argument "return" is reserved.  "return" is a reserved word in many languages so it is unlikely you will try to use it, but in languages where it might be legal, no caffeine method can have an argument called "return".

Types that begin with "_" are reserved.  You cannot have a type called "_int", for example.


### Class methods (e.g. static methods)

To invoke a static method, send:

* `_c`: the name of the class
* `_s`: the name of the method
* `_a`: The arguments.  Caffeine accepts only keyword arguments as a dictionary.

