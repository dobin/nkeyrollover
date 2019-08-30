
from enum import Enum

class MessageType(Enum): 
    PlayerKeypress = 0
    PlayerLocation = 1
    PlayerAttack = 2

    EnemyAttack = 3
    EnemyLocation = 4
    EnemyStateUpdate = 5



class Message(object): 
    def __init__(self, messageType, data): 
        self.messageType = messageType
        self.data = data


class Messaging(object):
    def __init__(self): 
        self.messages = []

    def add(self, message):
        self.messages.append(message)

    def reset(self): 
        self.messages.clear()

    def get(self): 
        return self.messages