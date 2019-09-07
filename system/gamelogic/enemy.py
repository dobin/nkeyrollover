import logging

from entities.enemy.enemyinfo import EnemyInfo

logger = logging.getLogger(__name__)


class Enemy():
    def __init__(self, name):
        self.isPlayer = False
        self.name :str = 'Bot' + name
        self.enemyInfo :EnemyInfo = EnemyInfo()


    def advance(self, deltaTime :float):
        pass


    def __repr__(self):
        return self.name
