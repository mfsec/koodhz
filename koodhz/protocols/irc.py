"""IRC protocol module"""

from abstract import AbstractProtocol

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl

from koodhz import router


class IrcProtocol(AbstractProtocol):
    """the irc prococol class"""

    def __init__(self, settings):
        super(IrcProtocol, self).__init__(settings)
        server = self._settings["irc.server"]
        factory = IrcProtocolFactory(settings)
        reactor.connectSSL(server, 6697, factory, ssl.ClientContextFactory())
        reactor.run()


class IrcProtocolFactory(AbstractProtocol, protocol.ClientFactory):
    """A factory for IrcBot.
       A new protocol instance will be created each time we connect
       to the server.
    """

    def __init__(self, settings):
        super(IrcProtocolFactory, self).__init__(settings)

    def buildProtocol(self, settings):
        """we build the IRC protocol handler"""
        p = IrcProtocolHandler(self._settings)
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        """we got disconnected from the ircd"""
        reactor.stop()


class IrcProtocolHandler(AbstractProtocol, irc.IRCClient):
    """IrcProtocol handler"""

    def __init__(self, settings):
        super(IrcProtocolHandler, self).__init__(settings)
        self.nickname = self._settings["irc.nickname"]
        self.identifier = "irc"

    def connectionMade(self):
        """we made a connection to the server"""
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        """we lost the connection to the ircd"""
        router.unregister(self)
        irc.IRCClient.connectionLost(self, reason)

    def joined(self, channel):
        """joined the channel"""
        router.register(self)

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        channel = self._settings["irc.channel"]
        self.join(channel)

    def send_message(self, message):
        """send a message to the irc channel on the config file"""
        channel = self._settings["irc.channel"]
        self.say(channel, message)

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""
        if channel == self.nickname:
            return
        user = user.split('!', 1)[0]
        router.relay(self, "%s: %s" % (user, msg))

    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'
