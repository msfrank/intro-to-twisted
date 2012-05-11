==================================
Structure of a Twisted application
==================================

The twisted API is quite large, but there are only a few significant pieces you
need to understand to begin using the framework; the vast majority of the API
are implementations of these pieces.

-----------
The reactor
-----------

The twisted reactor is also known as the event loop.  The reactor is responsible
for waiting for events to happen and dispatching callbacks to 'react' to these
events.  Using the reactor is a simple matter of importing the reactor module, and
calling run().

The reactor has methods to register interest in file descriptors, schedule timers,
work with threads, and open sockets, among other things.  However, this is all
fairly low-level; usually you will work with protocol specific classes which
abstract many of the nitty-gritty details.

One interesting thing to note is that there are actually multiple reactor backends,
which may be useful depending on your program.  For example, there is a gtk2 reactor
which integrates with the glib event loop, making it easy to use twisted in a pygtk
application.  Different platforms also may utilize different reactors, such as epoll
on Linux, kqueues on BSD variants, and win32 on Windows.

-----------
The Factory
-----------

Remember how I said that you will not work much with the reactor directly?  There
is one big exception to that statement: opening a listening or connect socket.
Twisted expects two parameters when you do so, a port number and an instance of a
Factory.  Usually you will subclass the twisted Factory class, and override the
buildProtocol() method.  When events of interest occur on the socket (an incoming
connection for a listening socket, and a completed connection on a connect socket),
the Factory buildProtocol() method is executed, which is expected to return a new
Protocol instance.

------------
The Protocol
------------

The Protocol is where your business logic resides.  Usually you will subclass
directly from the Protocol class, and override its methods dataReceived() and
connectionLost().  As described above, a Protocol instance is created every time a
new connection is made, and exists only for the lifetime of the connection.  This
is in contrast to the Factory instance, which lasts until the socket is closed.
