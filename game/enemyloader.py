import yaml
import logging

from game.enemytype import EnemyType
from system.gamelogic.weapontype import WeaponType
from texture.character.charactertexturetype import CharacterTextureType
from ai.enemyinfo import EnemyInfo
from .enemyseed import EnemySeed

logger = logging.getLogger(__name__)


class EnemyLoader(object):
    def __init__(self):
        self.enemySeeds = {}
        self.loadEnemies()


    def loadEnemies(self):
        for enemyType in EnemyType:
            enemySeed = self.loadEnemy(enemyType)
            self.enemySeeds[enemyType] = enemySeed


    def loadEnemy(self, enemyType):
        filename = "data/enemies/{}.yaml".format(enemyType.name)
        enemySeed = EnemySeed()

        with open(filename, 'r') as stream:
            data = yaml.safe_load(stream)

        enemySeed.characterTextureType = CharacterTextureType[data['characterTextureType']]
        enemySeed.weaponType = WeaponType[data['weaponType']]
        enemySeed.health = data['health']
        enemySeed.stunTime = data['stunTime']
        enemySeed.stunCount = data['stunCount']
        enemySeed.stunTimeFrame = data['stunTimeFrame']

        if 'attackBaseLocation' in data:
            enemySeed.attackBaseLocation = data['attackBaseLocation']
        else:
            enemySeed.attackBaseLocation = {
                'x': -1,
                'y': 1
            }

        enemyInfo = data['enemyInfo']
        try:
            enemySeed.enemyInfo.attackWindupTime = enemyInfo['attackWindupTime']
            enemySeed.enemyInfo.attackTime = enemyInfo['attackTime']
            enemySeed.enemyInfo.dyingTime = enemyInfo['dyingTime']
            enemySeed.enemyInfo.enemyCanAttackPeriod = enemyInfo['enemyCanAttackPeriod']
            enemySeed.enemyInfo.wanderTime = enemyInfo['wanderTime']
            enemySeed.enemyInfo.wanderTimeRnd = enemyInfo['wanderTimeRnd']
            enemySeed.enemyInfo.wanderStepDelay = enemyInfo['wanderStepDelay']
            enemySeed.enemyInfo.chaseTime = enemyInfo['chaseTime']
            enemySeed.enemyInfo.chaseTimeRnd = enemyInfo['chaseTimeRnd']
            enemySeed.enemyInfo.chaseStepDelay = enemyInfo['chaseStepDelay']
            enemySeed.enemyInfo.attackWindupTime = enemyInfo['attackWindupTime']
        except KeyError as error:
            raise Exception("Error, missing field in yaml file {}, error {}".format(
                filename, error
            ))

        return enemySeed


    def getSeedForEnemy(self, enemyType):
        return self.enemySeeds[enemyType]
