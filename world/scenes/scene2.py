import logging
import random

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
    def __init__(self, id, characterType, spawnTime, spawnX, spawnLocation):
        self.id = id
        self.characterType :CharacterType = characterType
        self.spawnTime = spawnTime
        self.spawnX = spawnX
        self.spawnLocation = spawnLocation


    def __repr__(self): 
        return "{} {} @{} @{} @{}".format(
            self.id,
            self.characterType, 
            self.spawnTime,
            self.spawnX, 
            self.spawnLocation)

        

class Scene2(SceneBase):
    def __init__(self, viewport, esperWorld):
        super().__init__(esperWorld=esperWorld, viewport=viewport)
        self.name = "Scene2 - Map 0x01"
        self.isShowPlayer = True
        self.isShowMap = True      

        self.enemyQueue = deque()
        
        self.maxEnemies = 6
        self.minEnemies = 4
        self.maxEnemiesAttacking = 2
        self.maxEnemiesChasing = 4

        self.time = 0.0
        self.enemyCount = 0

        self.prepareEnemies()


    def prepareEnemies(self): 
        waveIdx = 0
        waveCount = 3
        while waveIdx < waveCount:
            self.prepareWave(waveIdx, self.enemyQueue)
            waveIdx += 1


    def prepareWave(self, waveIdx, enemyQueue):
        intraWaveSpawnTime = 3
        intraWaveXoffset = 50

        # stickfigures
        n = 0
        while n < 10:
            playerTrapX = waveIdx * intraWaveXoffset 
            spawnLocation = self.getRandomSpawnCoords()
            enemyCell = EnemyCell(
                id = self.enemyCount,
                characterType = CharacterType.stickfigure,
                spawnTime = waveIdx * intraWaveSpawnTime,
                spawnX = playerTrapX,
                spawnLocation = spawnLocation,
            )
            self.enemyCount += 1
            enemyQueue.append(enemyCell)
            n += 1

        # cows
        n = 0
        while n < 2:
            playerTrapX = waveIdx * intraWaveXoffset 
            spawnLocation = self.getRandomSpawnCoords()
            enemyCell = EnemyCell(
                id = self.enemyCount,
                characterType = CharacterType.stickfigure,
                spawnTime = waveIdx * intraWaveSpawnTime,
                spawnX = playerTrapX,
                spawnLocation = spawnLocation,
            )
            self.enemyCount += 1
            enemyQueue.append(enemyCell)
            n += 1


    def spawnEnemy(self, enemyCell): 
        #logging.info("AAA: " + str(len(self.enemyQueue)))
        messaging.add(
            type=MessageType.SpawnEnemy,
            data=enemyCell,
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
        if len(self.enemyQueue) == 0:
            return

        enemyCell = self.enemyQueue[0]
        if enemyCell.spawnX < playerPosition.x: 
            self.spawnEnemy(enemyCell)
            del self.enemyQueue[0]


    def handleTime(self): 
        if len(self.enemyQueue) == 0:
            return

        # spawn more enemies?
        enemyCell = self.enemyQueue[0]
        if enemyCell.spawnTime < self.time:
            self.spawnEnemy(enemyCell)
            del self.enemyQueue[0]


    def handleEnemyDeath(self): 
        pass


    def advance(self, dt): 
        self.time += dt


    def getRandomSpawnCoords(self):
        if Config.devMode:
            coordinates = Coordinates(
                x=40,
                y=10 + random.randrange(0, 10),
            )
            return coordinates

        side = random.choice([True, False])
        myx = 0
        if side:
            myx = self.viewport.getx() + Config.columns + 1
        else:
            myx = self.viewport.getx() - 1 #- enemy.texture.width

        minY = Config.areaMoveable['miny']
        maxY = Config.areaMoveable['maxy']
        myy = random.randint(minY, maxY)
        spawnCoords = Coordinates(myx, myy)
        return spawnCoords