import esper
import logging

from entities.characterstatus import CharacterStatus
from entities.enemy.enemyinfo import EnemyInfo

logger = logging.getLogger(__name__)


class Enemy():
    def __init__(self, player, name, world, viewport):
        self.enemyMovement :bool = True
        self.player = player #
        self.world = world #
        self.viewport = viewport #

        self.characterStatus = CharacterStatus()

        self.name :str = 'Bot' + name
        self.active = False
        self.enemyInfo :EnemyInfo = EnemyInfo()

        self.offensiveAttackEntity = None


    def advance(self, deltaTime :float):
        pass


    def __repr__(self):
        return self.name
