"""bot"""

from protocols import IrcProtocol
from protocols import WhatsAppProtocol

from config import Configuration

if __name__ == '__main__':
    # create app and run
    config = Configuration()
    whatsapp = WhatsAppProtocol(config)
    irc = IrcProtocol(config)
