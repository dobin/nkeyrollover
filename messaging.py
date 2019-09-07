import logging
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(Enum):
    PlayerKeypress = 0  # to move, use attacks, skills
    PlayerLocation = 1  # to guide enemy, move viewport
    PlayerAttack = 2  # change into attack animation, collision detection, and more

    EnemyAttack = 4  # for collision detection, damage
    EnemyLocation = 5  # (unused)

    EntityMoved = 7  # to update walking animation
    attackWindup = 8  # to start attackWindup animation (on specific enemy)
    EntityAttack = 9  # to start attack animation (on specific enemy)

    EntityStun = 10  # to play stun animation
    EntityDying = 11  # to play death animation

    SpawnPlayer = 12
    SpawnEnemy = 13

    EmitTextureMinimal = 14
    EmitTexture = 15
    EmitActionTexture = 16


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
        if groupId is None:
            logger.info("%-20s: %s" % (type.name, data))
        else:
            logger.info("%-16s%4i: %s" % (type.name, groupId, data))


    def reset(self):
        self.messages.clear()


    def get(self):
        return self.messages


    def getByType(self, messageType):
        n = 0
        while n < len(self.messages):
            if self.messages[n].type is messageType: 
                yield self.messages[n]
            n += 1


    def getByGroupId(self, groupId):
        n = 0
        while n < len(self.messages):
            if self.messages[n].groupId is groupId: 
                yield self.messages[n]
            n += 1


messaging = Messaging()