import esper
from enum import Enum 
import logging

from messaging import messaging, Messaging, Message, MessageType
from system.offensiveattack import OffensiveAttack

logger = logging.getLogger(__name__)


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
                self.handlePlayerKeypress(message.data)


    def handlePlayerKeypress(self, key):
        playerAttack = self.world.component_for_entity(self.playerAttackEntity, OffensiveAttack)

        if key == ord(' '):
            playerAttack.attack()

        if key == ord('1'):
            playerAttack.switchWeaponByKey('1')

        if key == ord('2'):
            playerAttack.switchWeaponByKey('2')

        if key == ord('3'):
            playerAttack.switchWeaponByKey('3')

        if key == ord('4'):
            playerAttack.switchWeaponByKey('4')