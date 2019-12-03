import logging
from enum import Enum

logger = logging.getLogger(__name__)


class DirectMessageType(Enum):
    activateSpeechBubble = 0
    movePlayer = 1
    moveEnemy = 2
    receiveDamage = 3


class DirectMessage(object):
    def __init__(self, groupId, type, data):
        self.groupId = groupId
        self.type = type
        self.data = data


class DirectMessaging(object):
    """Send a message directly to another virtual object (via groupid)
    Every message here is intended for exactly 1 (one) recipient.
    """
    def __init__(self):
        self.messages = []
        self.frame = 0


    def setFrame(self, frame):
        self.frame = frame


    def add(self, groupId, type, data):
        self.messages.append(DirectMessage(
            groupId = groupId,
            type = type,
            data = data
        ))
        logger.info("%4i: DirectMsg for %6i: type %s: %s" %
                    (self.frame, groupId, type.name, data))


    def getByType(self, messageType, keep=False):
        for message in self.messages:
            if message.type == messageType:
                msg = message
                if not keep:
                    self.messages.remove(message)
                yield msg


# singleton
directMessaging = DirectMessaging()
