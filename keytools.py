#!python3


def Y64(bytes):
    import base64
    return base64.b64encode(bytes).replace("/", "_").replace("=", "-").replace("+", ".")


def unY64(string):
    import base64
    string = string.replace("_", "/").replace("-", "=").replace(".", "+")
    return base64.b64decode(string)


def parseURL(string):
    """Returns a tuple suitable for decoding caffeine URLs
    (zeromq_url, z85_public,z85_private,z85_server)"""
    import urllib.parse
    result = urllib.parse.urlparse(string)
    zeromq_url = result.scheme + "://" + result.hostname
    if result.port:
        zeromq_url += ":" + str(result.port)
    import zmq.utils.z85
    z85_public = z85_private = z85_server = None
    if result.username:
        z85_public = zmq.utils.z85.encode(unY64(result.username))
    if result.password:
        z85_private = zmq.utils.z85.encode(unY64(result.password))
    if result.query:
        z85_server = zmq.utils.z85.encode(unY64(result.query))

    return (zeromq_url, z85_public, z85_private, z85_server)
