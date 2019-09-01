import logging
from enum import Enum

logger = logging.getLogger(__name__)

#uniqueId = 0
#def getUniqueId():
#    uniqueId += 1
#    return uniqueId

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

    def add(self, groupId, type, data): 
        self.messages.append(DirectMessage(
            groupId = groupId, 
            type = type,
            data = data
        ))
        logger.info("DirectMsg for {} type {}: {}".format(groupId, type.name, data))

    def get(self, messageType): 
        for message in self.messages: 
            if message.type == messageType: 
                msg = message 
                self.messages.remove(message)
                return msg

        return None


# singleton
directMessaging = DirectMessaging()