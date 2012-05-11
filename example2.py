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
