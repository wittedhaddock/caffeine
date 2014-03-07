#!python3
from setuptools import setup, find_packages
import os.path
import sys
from setuptools.command.install import install


def zeromq_check():
    # let's check zeromq install
    try:
        import zmq
        zmq.curve_keypair()
    except Exception as ex:
        print(
            "pyzmq isn't configured (reason: %s), let's try to install it..." %
            ex)
        os.system(
            "pip install https://pypi.python.org/packages/source/p/pyzmq/pyzmq-14.0.1.tar.gz#md5=c35fa03e58d48e6f3df2ab2c2dfa1413 --force-reinstall")

    try:
        import zmq
        zmq.curve_keypair()
    except Exception as ex:
        print(
            "pyzmq couldn't be installed correctly on your system (reason: %s).  This may be because you need to install libsodium or libzmq manually." %
            ex)


zeromq_check() #this is bad, but I dunno what else to do.  setuptools doesn't support post-install.
import caffeine #detect caffeine's version
setup(
    name="caffeine",
    version=caffeine.__version__,
    packages=find_packages(),
    install_requires=['u-msgpack-python>=1.6'],

)
