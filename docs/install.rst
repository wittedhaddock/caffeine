Installation
=============

Dependencies
+++++++++++++

caffeine requires Python 3.3.  There are no plans to support earlier versions of python.  Go install it.

caffeine has some other dependencies, particularly on pyzmq->libzmq->libsodium.  In general, the script :download:`mactricks.sh <../mactricks.sh>` on OSX, and the :download:`Dockerfile <../Dockertests>` on Linux are the way to resolve these.


Install
++++++++++++

Once dependencies are met, you can install with pip.  

.. code-block:: bash

     pip install path/to/release.gz



.. _development-mode:

Development mode
+++++++++++++++++

see :ref:`development-mode`

caffeine is alpha, which means it often requires getting your hands dirty.  For this reason you should familiarize yourself with how to install caffeine for development.

.. code-block:: bash

   curl -O http://path/to/caffeine.tar.gz
   tar xf caffeine.tar.gz
   cd caffeine
   python setup.py develop

You can read more about setuptools' `developer mode <https://pythonhosted.org/setuptools/setuptools.html#develop-deploy-the-project-source-in-development-mode>`_ if you like, but the short version is that rather than copying the caffeine files into the appropriate places on your system, it installs symlinks in those places that point to where you ran the command.  In this way you can simply edit the files in the folder and the other programs on your system get the changes immediately, avoiding the need to install/reinstall.