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

More than one callback (or errback) can be registered with a Deferred.
When there is more than callback, the return value for the first callback
is passed as the first parameter to the next callback, and so on until
all callbacks have been executed.

The biggest stumbling block with multiple callbacks is how errors are
handled.  Imagine callbacks and errbacks in a Deferred as two parallel
lists.  First the function which generated the Deferred calls either
Deferred.callback() or Deferred.errback(), depending on success or failure.
Let's assume callback() was called, so processing starts at the first
callback; if the callback succeeds, it proceeds to the next callback, but
if it fails proceeds to the *second* errback.  If the errback returns a
Failure object or raises an exception, then processing continues to the
next errback.  However, if the errback returns an object other than a
Failure (including None!) and doesn't raise an Exception, then processing
moves back to the callback chain, proceeding with the *third* callback.

A more thorough explanation of deferreds is available as part of the 
twisted documentation: http://twistedmatrix.com/documents/current/core/howto/defer.html
