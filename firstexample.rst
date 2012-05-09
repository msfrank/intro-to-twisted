================
A simple example
================

Let's dive straight in.  This code shows usage of the three main components
of a twisted application that were mentioned before: the rector, the Protocol,
and the Factory.

The following code will listen on port 1234, waiting for connections.  when
it receives a connection, it will accept it, and wait for data to come in.
When data arrives, it echoes it back to the client, then closes the
connection::

 from twisted.internet import protocol, reactor
 
 class Echo(protocol.Protocol):
     def dataReceived(self, data):
         self.transport.write(data)
         self.transport.loseConnection()
 
 class EchoFactory(protocol.Factory):
     def buildProtocol(self, addr):
         return Echo()
 
 reactor.listenTCP(1234, EchoFactory())
 reactor.run()
