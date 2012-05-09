=================================
What is event driven programming?
=================================

Wikipedia can give you a thorough definition:

http://en.wikipedia.org/wiki/Event-driven_programming

Event driven programming is based on callbacks.  You register callbacks to
specified events of interest, then hand off program control to the libraries'
run() function.  The library then executes the registered callbacks when
events occur.  Callbacks can be registered at any time, but are mostly registered
at the start of a program.

Event driven programming is useful when your application is based on waiting
for events.  Network programming is a canonical example:  you write data to a
remote server, then wait for data to come back.  On the other hand, applications
which are CPU-bound traditionally are not good candidates to implement using
event driven programming, because long linear sequences of code must be broken
up into chains of callbacks, which obscures and complicates the code.

Event driven programming is often single-threaded, although this is not always
the case.  When single-threaded, access to shared resources is simpler, since
within a single callback you know that no other code is possibly being executed
concurrently.
