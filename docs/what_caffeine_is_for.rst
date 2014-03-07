caffeine design goals
==================

caffeine has a few high-level design goals.

Pro-server
#########

Most BaaS tools that exist today have declared war on servers.  At the time of this writing, Parse's `marketing material <https://parse.com/products/core>`_ includes an image of a server in a trash can.  

While caffeine shares the perspective that today's servers are way too complex, frustrating, and far too much work, we think the solution is to make servers better instead of throwing them away.

This principle impacts the design of many features, including:

* Letting you write server-side code in a Real Actual Server Language (Python3)
* Self-hosting as a first-class citizen.  caffeine can run anywhere, from AWS to DigitalOcean to your corporate datacenter to your basement.  You can spin up servers on your Jenkins install, or run a server locally to work offline.
* Emphasizing writing server code where that works best, instead of shoehorning everything into the client

Fast
##########

caffeine is in the unique position of being on both ends of the network pipe.  This is an opportunity to rethink internet communicatons for the first time in decades.

caffeine uses a modern, high-performance network stack designed to meet the needs of modern applications.  It uses some of the same technology that you may have seen in super-low-latency apps like Spotify, except now you can get that speed for your own applications.

For that and other reasons, caffeine is breathtakingly fast compared to what you're doing now, and it gets faster with each release.  Just recompile.

Compress your brain
###################

To write modern client/server applications, you have to know a lot of things.  HTTP.  REST.  JSON.  OAuth.  Caching.  Timeouts.  Locking.  Nginx.  Load balancing.  API design.  Deployment tools.  Databases.

caffeine's goal is to significantly reduce the amount of stuff you need to know just to get some data from a server, and in doing so cancel all those pesky planning meetings between client/server teams.  This significantly increases how fast you can add features and iterate your project.


