import esper
import logging

from utilities.entityfinder import EntityFinder
from messaging import messaging, MessageType
from system.gamelogic.offensiveattack import OffensiveAttack
import system.groupid

logger = logging.getLogger(__name__)


class OffensiveAttackProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        self.handlePlayerAttackKeyPressMessage()
        self.advance(dt)


    def advance(self, dt):
        for ent, offensiveAttack in self.world.get_component(OffensiveAttack):
            offensiveAttack.advance(dt)


    def handlePlayerAttackKeyPressMessage(self):
        for message in messaging.getByType(MessageType.PlayerKeypress):
            self.handlePlayerKeypress(message.data['key'])


    def handlePlayerKeypress(self, key):
        playerAttack, mePlayer = self.getPlayerAttack()
        if playerAttack is None:
            # No player here yet
            return

        # can change weapon even when attacking
        if key == ord('1'):
            playerAttack.switchWeaponByKey('1')

        if key == ord('2'):
            playerAttack.switchWeaponByKey('2')

        if key == ord('3'):
            playerAttack.switchWeaponByKey('3')

        if key == ord('4'):
            playerAttack.switchWeaponByKey('4')

        if not mePlayer.isAttacking:
            if key == ord(' '):
                playerAttack.attack()

        # if key == ord('t'):
        if key == -301:  # tab
            playerAttack.showBuckler()


    def getPlayerAttack(self):
        # find player
        playerEntity = EntityFinder.findPlayer(self.world)
        if playerEntity is None:
            return None, None

        mePlayer = self.world.component_for_entity(
            playerEntity, system.gamelogic.player.Player)

        # find characterattack for player
        meGroupId = self.world.component_for_entity(
            playerEntity, system.groupid.GroupId)
        ret = EntityFinder.findOffensiveAttackByGroupId(self.world, meGroupId.getId())

        return ret, mePlayer
