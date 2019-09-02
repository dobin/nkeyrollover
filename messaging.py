import logging
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(Enum): 
    PlayerKeypress = 0
    PlayerLocation = 1
    PlayerAttack = 2

    EnemyAttack = 4 # for collision detection, damage
    EnemyLocation = 5

    EntityMoved = 7 # to update walking animation
    attackWindup = 8 # to start attackWindup animation (on specific enemy)
    EntityAttack = 9 # to start attack animation (on specific enemy)


class Message(object): 
    def __init__(self, type, data, groupId): 
        self.type = type
        self.data = data
        self.groupId = groupId


class Messaging(object):
    """Deliver messages to 0-n recipients
    This queue will be emptied upon each iteration / frame. 
    See world esper processors for the order in which messages can be sent
    (only downward)
    """
    def __init__(self): 
        self.messages = []


    def add(self, type, data, groupId=None):
        self.messages.append(Message(
            type=type,
            data=data,
            groupId=groupId,
        ))
        logger.info("Msg for {} type {}: {}".format(groupId, type.name, data))


    def reset(self):
        self.messages.clear()


    def get(self): 
        return self.messages


messaging = Messaging()