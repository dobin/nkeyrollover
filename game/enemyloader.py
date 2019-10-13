import yaml
import logging

from game.enemytype import EnemyType
from system.gamelogic.weapontype import WeaponType
from texture.character.charactertexturetype import CharacterTextureType
from ai.enemyinfo import EnemyInfo
from .enemyseed import EnemySeed
from common.direction import Direction
from texture.filetextureloader import fileTextureLoader
from texture.character.characteranimationtype import CharacterAnimationType


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
        enemySeed.knockdownChance = data['knockdownChance']

        if 'attackBaseLocation' in data:
            enemySeed.attackBaseLocation = data['attackBaseLocation']
        else:
            enemySeed.attackBaseLocation = {
                'x': -1,
                'y': 1
            }

        enemyInfo = data['enemyInfo']
        try:
            enemySeed.enemyInfo.enemyType = enemyType
            enemySeed.enemyInfo.attackWindupTime = enemyInfo['attackWindupTime']
            enemySeed.enemyInfo.attackStateTime = enemyInfo['attackStateTime']

            enemySeed.enemyInfo.enemyCanAttackPeriod = enemyInfo['enemyCanAttackPeriod']
            enemySeed.enemyInfo.wanderTime = enemyInfo['wanderTime']
            enemySeed.enemyInfo.wanderTimeRnd = enemyInfo['wanderTimeRnd']
            enemySeed.enemyInfo.wanderStepDelay = enemyInfo['wanderStepDelay']
            enemySeed.enemyInfo.chaseTime = enemyInfo['chaseTime']
            enemySeed.enemyInfo.chaseTimeRnd = enemyInfo['chaseTimeRnd']
            enemySeed.enemyInfo.chaseStepDelay = enemyInfo['chaseStepDelay']
            enemySeed.enemyInfo.attackWindupTime = enemyInfo['attackWindupTime']

            # set state_dying length to dying animation length
            animation = fileTextureLoader.characterAnimationManager.getAnimation(
                characterTextureType=enemySeed.characterTextureType,
                characterAnimationType=CharacterAnimationType.dying,
                direction=Direction.left,
            )
            enemySeed.enemyInfo.dyingTime = animation.getAnimationLength()

            # optionals
            if 'attackTime' in enemyInfo:
                enemySeed.enemyInfo.attackTime = enemyInfo['attackTime']
            else:
                enemySeed.enemyInfo.attackTime = enemySeed.enemyInfo.attackStateTime

            if 'wanderAttackDistance' in enemyInfo:
                enemySeed.enemyInfo.wanderAttackDistance = enemyInfo['wanderAttackDistance']

        except KeyError as error:
            raise Exception("Error, missing field in yaml file {}, error {}".format(
                filename, error
            ))

        return enemySeed


    def getSeedForEnemy(self, enemyType):
        return self.enemySeeds[enemyType]
