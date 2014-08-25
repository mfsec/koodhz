"""router module"""


class Router:
    """routing class"""

    def __init__(self):
        self.protocolInstances = {}

    def register(self, protocol):
        """register a protocol"""
        self.protocolInstances[protocol.identifier] = protocol

    def isRegistered(self, protocol):
        """check if the protocol is already registed"""
        return protocol.identifier in self.protocolInstances

    def unregister(self, protocol):
        """unregister the protocol"""
        if protocol.identifier not in self.protocolInstances:
            return
        del self.protocolInstances[protocol.identifier]

    def relay(self, protocol, message):
        """relay the message"""
        print message
        for identifier in self.protocolInstances.keys():
            if identifier == protocol.identifier:
                continue
            instance = self.protocolInstances[identifier]
            instance.send_message(message)
