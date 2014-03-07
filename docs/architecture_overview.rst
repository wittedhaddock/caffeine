Architecture overview
++++++++++++++++++++++

Basic principles
=======================
.. graphviz::

   digraph architecture {
   				rankdir=LR

   compound=true;
   node [shape=record fontsize=10 fontname="Verdana"];

      subgraph cluster_s1 {
        "router"
      	label = "server"
      	subgraph cluster_w1 {
	      	label = "worker"
	      	CC1 [label="custom code"]
	      }
	      subgraph cluster_w2 {
	      	label = "worker"
	      	CC2 [label="custom code"]
	      }
      }
      subgraph cluster_client {
    	subgraph cluster_libcaffeineios {
    		label = "libcaffeine-ios"
    		"ORM"
    		"CaffeineClient"

    		ORM->CaffeineClient

    	}
        "your code"->"ORM"
        "your code"->"stubs"
        "stubs"->"CaffeineClient"
        CaffeineClient->router [style=dashed,color=red]
      	label = "client"
      }

      
      subgraph cluster_s2 {
        "router"
      	label = "server"
	      subgraph cluster_w3 {
	      	label = "worker"
	      	CC3 [label="custom code"]
	      }
	   }
        router -> CC1 [lhead=cluster_w1,style=dashed,color=red]
      	router -> CC2 [lhead=cluster_w2,style=dashed,color=red]
      	router -> CC3 [lhead=cluster_w3,style=dashed,color=red]

      	//virtual paths
      	"stubs"->"CC3" [style=dotted]
      	"stubs"->CC1 [style=dotted]
      	stubs->CC2 [style=dotted]

      	subgraph cluster_legend {
      	    node [label=""]
      	    label="legend"

      		EX1->EX2 [label="API boundary"]
      		EX3->EX4 [label="network boundary",style=dashed,color=red]
      		EX5->EX6 [label="logical path",style=dotted]


      	}
   }

Vocabulary
===========

.. glossary:: 

  client
    This is a client process, like an iOS app.

  stub
    These are stub header files for remote objects.  These are generated with the :py:class:`caffeine.codegen` tool.

  ORM

    ORM is not included in this release.

  CaffeineClient

    This ObjC component implements the caffeine wire protocol.

  server

    A physical server machine

  router

    A router process. The module :class:`caffeine.router` is such a process.

  worker

    A worker process.  A worker process spawns an instance of :class:`caffeine.worker.RPCWorker`

    Worker processes are how Python's GIL is defeated.  A worker process can run on the same server as the router or a different server.

  custom code

    A function you write that handles the request.





