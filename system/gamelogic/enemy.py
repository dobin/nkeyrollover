import esper
import logging

from entities.enemy.enemyinfo import EnemyInfo

logger = logging.getLogger(__name__)


class Enemy():
    def __init__(self, name):
        self.enemyMovement :bool = True

        self.name :str = 'Bot' + name
        self.enemyInfo :EnemyInfo = EnemyInfo()

        self.offensiveAttackEntity = None


    def advance(self, deltaTime :float):
        pass


    def __repr__(self):
        return self.name
