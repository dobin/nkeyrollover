import esper
import logging

from messaging import messaging, MessageType
from system.gamelogic.offensiveskill import OffensiveSkill
import system.groupid
from utilities.entityfinder import EntityFinder

logger = logging.getLogger(__name__)


class OffensiveSkillProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        self.handleAttackKeyPress()
        self.advance(dt)


    def advance(self, dt):
        for ent, offensiveSkill in self.world.get_component(OffensiveSkill):
            offensiveSkill.advance(dt)


    def handleAttackKeyPress(self):
        for message in messaging.getByType(MessageType.PlayerKeypress):
            self.handlePlayerKeypress(message.data['key'])


    def handlePlayerKeypress(self, key):
        playerSkill = self.getPlayerSkill()
        if playerSkill is None:
            # no player here yet
            return

        if key == ord('c'):
            playerSkill.doSkill('c')

        if key == ord('f'):
            playerSkill.doSkill('f')

        if key == ord('g'):
            playerSkill.doSkill('g')

        if key == ord('q'):
            playerSkill.doSkill('q')

        if key == ord('w'):
            playerSkill.doSkill('w')

        if key == ord('e'):
            playerSkill.doSkill('e')

        if key == ord('r'):
            playerSkill.doSkill('r')


    def getPlayerSkill(self):
        playerEntity = EntityFinder.findPlayer(self.world)
        if playerEntity is None:
            return None

        meGroupId = self.world.component_for_entity(
            playerEntity, system.groupid.GroupId)

        offensiveSkillEntity = EntityFinder.findOffensiveSkillByGroupId(
            self.world,
            meGroupId.getId())

        return offensiveSkillEntity
