import logging

from utilities.timer import Timer
from world.scenes.scenebase import SceneBase
from sprite.coordinates import Coordinates
from system.renderable import Renderable
from texture.phenomena.phenomenatype import PhenomenaType
from texture.phenomena.phenomenatexture import PhenomenaTexture
from messaging import messaging, MessageType
from collections import deque
from config import Config
from texture.character.charactertype import CharacterType

logger = logging.getLogger(__name__)


class EnemyCell(object): 
    def __init__(self, characterType, spawnTime, spawnX):
        self.characterType :CharacterType = None
        self.spawnTime = spawnTime
        self.spawnX = spawnX

        

class Scene2(SceneBase):
    def __init__(self, viewport, esperWorld):
        super().__init__(esperWorld=esperWorld, viewport=viewport)
        self.name = "Scene2 - Map 0x01"
        self.isShowPlayer = True
        self.isShowMap = True      

        self.enemyQueue = deque()
        self.prepareEnemies()

        self.maxEnemies = 6
        self.minEnemies = 4
        self.maxEnemiesAttacking = 2
        self.maxEnemiesChasing = 4

        self.time = 0.0


    def prepareEnemies(self): 
        waveIdx = 0
        waveCount = 4
        while waveIdx < waveCount:
            self.prepareWave(waveIdx, self.enemyQueue)
            waveIdx += 1


    def prepareWave(self, waveIdx, enemyQueue):
        intraWaveSpawnTime = 3
        intraWaveXoffset = 120 # a bit over screen length

        n = 0
        while n < 10:
            enemyCell = EnemyCell(
                characterType = CharacterType.stickfigure,
                spawnTime = waveIdx * intraWaveSpawnTime,
                spawnX = waveIdx * intraWaveXoffset
            )
            enemyQueue.append(enemyCell)
            n += 1

        n = 0
        while n < 2:
            enemyCell = EnemyCell(
                characterType = CharacterType.stickfigure,
                spawnTime = waveIdx * intraWaveSpawnTime,
                spawnX = waveIdx * intraWaveXoffset
            )
            enemyQueue.append(enemyCell)
            n += 1


    def spawnEnemy(self, enemyCell): 
        messaging.add(
            type=MessageType.SpawnPlayer,
            data={
                'enemyCell': enemyCell,
            },

        )

    def spawnPlayer(self):
        coordinates = Coordinates(24, 13)
        messaging.add(
            type=MessageType.SpawnPlayer,
            data={
                'coordinates': coordinates
            },
        )


    def enter(self):
        self.time = 0.0
        self.spawnPlayer()


    def handlePosition(self, playerPosition, viewportX):
        # spawn more enemies?
        # note that will not spawn all enemies at a certain position at once, 
        # but only on every move of the player
        enemyCell = self.enemyQueue[0]
        if enemyCell.x < playerPosition.x: 
            self.spawnEnemy(enemyCell)
            del enemyCell


    def handleTime(self): 
        # spawn more enemies?
        enemyCell = self.enemyQueue[0]
        if enemyCell.spawnTime < self.time:
            self.spawnEnemy(enemyCell)
            del enemyCell

    def handleEnemyDeath(self): 
        pass


    def advance(self, dt): 
        self.time += dt

