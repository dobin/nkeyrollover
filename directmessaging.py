import logging
from enum import Enum

logger = logging.getLogger(__name__)

#uniqueId = 0
#def getUniqueId():
#    uniqueId += 1
#    return uniqueId


class DirectMessage(object): 
    def __init__(self, groupId, data): 
        self.groupId = groupId
        self.data = data


class DirectMessaging(object): 
    def __init__(self):
        self.messages = []

    def add(self, groupId, data): 
        self.messages.append(DirectMessage(
            groupId = groupId, 
            data = data
        ))

    def get(self, groupId): 
        for message in self.messages: 
            if message. groupId == groupId: 
                msg = message 
                self.messages.remove(message)
                return msg


directMessaging = DirectMessaging()