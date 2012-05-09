=================
More on Deferreds
=================

I mentioned that Deferreds have features beyond that of a simple callback.
In this section, i will explain a few.

--------------
Error Handling
--------------

First, a Deferred has error handling.  In addition to registering a callback,
you can register an 'errback', which will be called in the event of an error.
The first parameter to an errback function is a Failure object, which is
basically an Exception.

Let's update the proxy example with some error handling- if the getPage()
function generates an error, then display the error message to the client and
print the error message to stdout::
 
 from twisted.internet import protocol, reactor
 from twisted.web.client import getPage
 
 class Proxy(protocol.Protocol):
     def dataReceived(self, data):
         url = data.strip()
         print "retrieving url %s" % url
         d = getPage(url)
         d.addCallback(self.displayPage)
         d.addErrback(self.handleError)
 
     def displayPage(self, result):
         self.transport.write(result)
         self.transport.loseConnection()
 
     def handleError(self, failure):
         print "error: %s" % failure.getErrorMessage()
         self.transport.write("error: %s\n" % failure.getErrorMessage())
         self.transport.loseConnection()
 
 class ProxyFactory(protocol.Factory):
     def buildProtocol(self, addr):
         return Proxy()
 
 reactor.listenTCP(1234, ProxyFactory())
 reactor.run()

------------------
Multiple Callbacks
------------------


