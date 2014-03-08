caffeine
============

.. image:: docs/caffeinelogo.png


caffeine is a backend-in-a-box that is designed for the applications of tomorrow.  Caffeine covers a lot of ground, but you can think of it as an alternative to BaaS_ offerings like like Parse_, StackMob_, Firebase_, and `iCloud Core Data`_, to web service schemes like XMLRPC_, Thrift_, and REST_, and to networking libraries like AFNetworking_.  

.. _BaaS: http://en.wikipedia.org/wiki/Backend_as_a_service
.. _Parse: http://parse.com
.. _StackMob: https://www.stackmob.com
.. _Thrift: http://thrift.apache.org
.. _XMLRPC: http://en.wikipedia.org/wiki/XML-RPC
.. _REST: http://en.wikipedia.org/wiki/Representational_state_transfer
.. _iCloud Core Data: https://developer.apple.com/library/ios/documentation/General/Conceptual/iCloudDesignGuide/Chapters/DesignForCoreDataIniCloud.html
.. _AFNetworking: https://github.com/AFNetworking/AFNetworking
.. _Firebase: https://www.firebase.com

If you're interested in seeing how caffeine compares to other software, see our `design goals <http://caffeine.readthedocs.org/en/latest/what_caffeine_is_for.html>`_.

License
=========

Although caffeine is open source, it's a commercial project, and we're `still figuring out a fair way to license it <https://github.com/drewcrawford/caffeine/issues/1>`_.  In the meantime, if you want to use caffeine in a real project contact `the author <mailto:drew@sealedabstract.com>`_.  I don't bite.

Documentation
==============

caffeine has more `reasonable documentation than you'd expect <http://caffeine.readthedocs.org>`_.

Build status
============

"up" suite: |up|

.. |up| image:: http://teamcity.drewcrawfordapps.com:8111/app/rest/builds/buildType:(id:caffeine_Dockerup)/statusIcon 
			:target: http://teamcity.drewcrawfordapps.com:8111/viewType.html?buildTypeId=Caffeine_Dockerup&guest=1

"ios" suite: |ios|

.. |ios| image:: http://teamcity.drewcrawfordapps.com:8111/app/rest/builds/buildType:(id:CaffeineIos_Analyze)/statusIcon 
			:target: http://teamcity.drewcrawfordapps.com:8111/viewType.html?buildTypeId=CaffeineIos_Analyze&guest=1

"tests" suite: |tests|

.. |tests| image:: http://teamcity.drewcrawfordapps.com:8111/app/rest/builds/buildType:(id:caffeine_Dockertests)/statusIcon 
			:target: http://teamcity.drewcrawfordapps.com:8111/viewType.html?buildTypeId=caffeine_Dockertests&guest=1

Release History
=================
* 0.1 "Tieguanyin" (2013) private proof-of-concept

Roadmap
=========

* 0.2 "Tarrazu" (March 2014, TBA) RPC
* 0.3 (TBA) security-focused release
* 0.4 (TBA) ORM-focused release


