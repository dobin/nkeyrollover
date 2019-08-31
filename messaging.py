import logging
from enum import Enum

logger = logging.getLogger(__name__)


class MessageType(Enum): 
    PlayerKeypress = 0
    PlayerLocation = 1
    PlayerAttack = 2

    EnemyAttack = 3
    EnemyLocation = 4
    EnemyStateUpdate = 5


class Message(object): 
    def __init__(self, type, data): 
        self.type = type
        self.data = data


class Messaging(object):
    def __init__(self): 
        self.messages = []

    def add(self, type, data):
        self.messages.append(Message(
            type=type,
            data=data
        ))
        logging.info("Msg {}: {}".format(type, data))

    def reset(self): 
        self.messages.clear()

    def get(self): 
        return self.messages

messaging = Messaging()