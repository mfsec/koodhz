"""WhatsApp protocol module"""

from abstract import AbstractProtocol
from koodhz.Yowsup.connectionmanager import YowsupConnectionManager
import base64
from koodhz import router


class WhatsAppProtocol(AbstractProtocol):
    """WhatsApp Protocol"""

    def __init__(self, settings):
        super(WhatsAppProtocol, self).__init__(settings)

        self.identifier = "whatsapp"
        self.username = self._settings["whatsapp.username"]
        passwd_ = self._settings["whatsapp.password"]
        self.password = base64.b64decode(bytes(passwd_.encode('utf-8')))

        connection_manager = YowsupConnectionManager()
        self.signalsInterface = connection_manager.getSignalsInterface()
        self.methodsInterface = connection_manager.getMethodsInterface()
        self.register_signals()
        self.methodsInterface.call("auth_login", (self.username,
                                                  self.password))

    def register_signals(self):
        """register the signals"""
        signals = [
            ("auth_fail", self.auth_fail),
            ("auth_success", self.auth_success),
            ("message_received", self.message_received),
            ("group_messageReceived", self.group_messageReceived),
            ("group_imageReceived", self.group_imageReceived),
        ]

        for signal, handler in signals:
            self.signalsInterface.registerListener(signal, handler)

    def group_messageReceived(self, messageId, jid, author, messageContent,
                              timestamp, wantsReceipt, pushName):
        """event on recive group message"""
        router.relay(self, "%s: %s" % (author, messageContent))
        self.methodsInterface.call("message_ack", (jid, messageId))

    def message_received(self, messageId, jid, messageContent, timestamp,
                         wantsReceipt, pushName, isBroadCast):
        """event on recive normal message"""
        router.relay(self, "%s: %s" % (jid, messageContent))
        self.methodsInterface.call("message_ack", (jid, messageId))

    def group_imageReceived(self, msgId, fromAttribute, author, mediaPreview,
                            mediaUrl, mediaSize, wantsReceipt):
        """event on recive a image file"""
        router.relay(self, "%s: %s" % (author, mediaUrl))
        self.methodsInterface.call("message_ack", (fromAttribute, msgId))

    def auth_fail(self, username, reason):
        """event on authentication fail"""
        router.unregister(self)

    def auth_success(self, username):
        """event on auth sucess"""
        router.register(self)
        self.methodsInterface.call("ready")

    def send_message(self, text):
        """send message to the group setted on the config"""
        print "senasdasd", text
        jid = self._settings["whatsapp.gid"]
        self.methodsInterface.call("message_send", (jid, text))
