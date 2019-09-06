import esper
import logging

from utilities.entityfinder import EntityFinder
from messaging import messaging, Messaging, Message, MessageType
from system.offensiveattack import OffensiveAttack
import system.groupid

logger = logging.getLogger(__name__)


class OffensiveAttackProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        self.handleAttackKeyPress()
        self.advance(dt)


    def advance(self, dt):
        for ent, offensiveAttack in self.world.get_component(OffensiveAttack):
            offensiveAttack.advance(dt)


    def handleAttackKeyPress(self):
        for message in messaging.getByType(MessageType.PlayerKeypress):
            self.handlePlayerKeypress(message.data['key'])


    def handlePlayerKeypress(self, key):
        playerAttack = self.getPlayerAttack()
        if playerAttack is None:
            # No player here yet
            return
        

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


    def getPlayerAttack(self):
        # find player
        playerEntity = EntityFinder.findPlayer(self.world)
        if playerEntity is None: 
            return None

        meGroupId = self.world.component_for_entity(
            playerEntity, system.groupid.GroupId)


        # find characterattack for player
        ret = EntityFinder.findOffensiveAttackByGroupId(self.world, meGroupId.getId())

        return ret
        
