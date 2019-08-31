import esper
from enum import Enum 
import logging

from messaging import messaging, Messaging, Message, MessageType
from system.offensiveattack import OffensiveAttack


class OffensiveAttackProcessor(esper.Processor):
    def __init__(self, playerAttackEntity):
        super().__init__()
        self.playerAttackEntity = playerAttackEntity


    def process(self, dt):
        self.handleAttackKeyPress()
        self.advance(dt)

    
    def advance(self, dt):
        for ent, offensiveAttack in self.world.get_component(OffensiveAttack):
            offensiveAttack.advance(dt)


    def handleAttackKeyPress(self):
        for message in messaging.get():
            if message.type is MessageType.PlayerKeypress: 
                if message.data == ord(' '):
                    playerAttack = self.world.component_for_entity(self.playerAttackEntity, OffensiveAttack)
                    playerAttack.attack()