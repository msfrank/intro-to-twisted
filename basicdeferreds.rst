===============
Using Deferreds
===============

The above example is a simple one: it waits for data from the client, then
performs its task returning a result immediately.  But any non-trivial program
will need to perform some business logic that will take a potentially
unbounded amount of time, such as communicating with a database.  If we
executed this logic synchronously, it will block the entire program until
completion.  This is not what we want, and this is where the twisted concept
of Deferreds come into play.

A Deferred is a callback, with extra features.  All functions in twisted which
could possibly block will instead immediately return a Deferred, and your
business logic then registers callbacks on the Deferred object.  Once the
blocking function has completed, it executes the callbacks registered with the
Deferred, passing in the result as the first parameter.

As an example, here is code for a extremely stupid HTTP proxy.  The code
listens for connections on port 1234, reads a url from the client, then
retrieves the url and returns the data back to the client::

 from twisted.internet import protocol, reactor
 from twisted.web.client import getPage
 
 class Proxy(protocol.Protocol):
     def dataReceived(self, data):
         url = data.strip()
         print "retrieving url %s" % url
         d = getPage(url)
         d.addCallback(self.displayPage)
 
     def displayPage(self, result):
         self.transport.write(result)
         self.transport.loseConnection()
 
 class ProxyFactory(protocol.Factory):
     def buildProtocol(self, addr):
         return Proxy()
 
 reactor.listenTCP(1234, ProxyFactory())
 reactor.run()
