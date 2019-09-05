import esper
import logging

from messaging import messaging, MessageType
from system.offensiveskill import OffensiveSkill

logger = logging.getLogger(__name__)


class OffensiveSkillProcessor(esper.Processor):
    def __init__(self, player):
        super().__init__()
        self.player = player


    def process(self, dt):
        self.handleAttackKeyPress()
        self.advance(dt)


    def advance(self, dt):
        for ent, offensiveSkill in self.world.get_component(OffensiveSkill):
            offensiveSkill.advance(dt)


    def handleAttackKeyPress(self):
        for message in messaging.getByType(MessageType.PlayerKeypress):
            self.handlePlayerKeypress(message.data)


    def handlePlayerKeypress(self, key):
        playerSkill = self.world.component_for_entity(self.player, OffensiveSkill)

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