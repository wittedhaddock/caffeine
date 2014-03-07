A sample caffeine project
==========================

Server
+++++++++

Let's create a simple project.  First, let's write a simple "hello world" :term:`worker`:

.. literalinclude:: ../examples/basic/worker.py

We can now run our worker:

.. code-block:: bash

   python3 worker.py

We will also launch the default caffeine router.

.. code-block:: bash

	caffeine_router

You will get some messages indicating that the router has started and is accepting requests.

Client
+++++++++++

First, let's create a basic iOS project.  File->New Project... you know the drill.

Next, we're going to pull down a release of `caffeine-ios <http://github.com/drewcrawford/caffeine-ios>`.

Then we will drag the caffeine-ios.xcodeproj into our current project or workspace...

.. image:: projectsetup.png

...and link it

.. image:: link1.png

.. image:: link2.png

We also need to
  * link with std++ (same dialog)
  * Add ``$CONFIGURATION_BUILD_DIR/include`` to your Header Search Paths.
  * Add ``-ObjC`` to our ``Other Linker Flags``

codegen
#############

We will use the :class:`caffeine.codegen` tool to generate :term:`stub` s.  

.. code-block:: bash

   caffeine_codegen --language objc -o path/to/output/directory --url="tcp://yxDrGth0x7Mp6gZdcb2iFymACxoPbXgbgMFT7rELGmI-:WSKWXvnHyF7_jNEchETg1NoZte6Nsd3htA4CWRqZv1A-@127.0.0.1:55555?yxDrGth0x7Mp6gZdcb2iFymACxoPbXgbgMFT7rELGmI-"

This URL looks kinda funny, and if you want to know more about it go read the docs about :doc:`/urls`.

After running this tool, you will get a few new .h and .m files, including ``Foo.h`` and ``Foo.m``.  Add those to your xcodeproject.  If you ensure that you pass the right directory to the ``-o`` flag, once added these files will update out from under xcode and will not require you to continually re-add them.

Use
###########

Now we can call our hello world from ObjC:

.. code-block:: objc

    NSError *err = nil;
    NSLog(@"%@",[Foo helloWorldWithError:&err]);


And out to the console we get:

.. code-block:: plain

    hello world

You can download the :download:`completed example project <basic.zip>`.


