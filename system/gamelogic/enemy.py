import logging

from ai.enemyinfo import EnemyInfo

logger = logging.getLogger(__name__)


class Enemy():
    def __init__(self, name :str, enemyInfo :EnemyInfo =None):
        self.isPlayer = False
        self.name :str = 'Bot' + name
        self.enemyInfo :EnemyInfo = enemyInfo


    def advance(self, deltaTime :float):
        pass


    def setEnemyInfo(self, enemyInfo :EnemyInfo):
        self.enemyInfo = enemyInfo


    def __repr__(self):
        return self.name
