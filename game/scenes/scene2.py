import logging
import random

from game.scenes.scenebase import SceneBase
from common.coordinates import Coordinates
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


class Akt(object):
    def __init__(self):
        self.min_x = 0
        self.max_x = 0
        self.enemyQueue = deque()


class Scene2(SceneBase):
    def __init__(self, viewport, world):
        super().__init__(world=world, viewport=viewport)
        self.name = "Scene2"
        self.isShowPlayer = True
        self.isShowMap = True

        self.enemyQueue = deque()
        self.enemySpawned = []

        self.maxEnemies = 6
        self.time = 0.0
        self.enemyCount = 0

        self.prepareEnemies()


    def prepareEnemies(self):
        waveIdx = 0
        waveCount = 3
        if Config.devMode:
            enemyCell = EnemyCell(
                id = self.enemyCount,
                characterType = CharacterType.dragon,
                spawnTime = None,
                spawnX = 0,
                spawnLocation = Coordinates(35, 13),
            )
            self.enemyQueue.append(enemyCell)

            enemyCell = EnemyCell(
                id = self.enemyCount,
                characterType = CharacterType.cow,
                spawnTime = None,
                spawnX = 0,
                spawnLocation = Coordinates(85, 13),
            )
            self.enemyQueue.append(enemyCell)

            enemyCell = EnemyCell(
                id = self.enemyCount,
                characterType = CharacterType.stickfigure,
                spawnTime = None,
                spawnX = 60,
                spawnLocation = Coordinates(60 + 80, 13),
            )
            self.enemyQueue.append(enemyCell)
            return

        while waveIdx < waveCount:
            self.prepareWave(waveIdx, self.enemyQueue)
            waveIdx += 1


    def prepareWave(self, waveIdx, enemyQueue):
        intraWaveSpawnTime = 3
        intraWaveXoffset = 50

        numStickfigures = 10
        numCows = 2

        # stickfigures
        n = 0
        while n < numStickfigures:
            playerTrapX = waveIdx * intraWaveXoffset
            spawnLocation = self.getRandomSpawnCoords(rightSideBias=0.8)
            enemyCell = EnemyCell(
                id = self.enemyCount,
                characterType = CharacterType.stickfigure,
                spawnTime = None,  # waveIdx * intraWaveSpawnTime + n,
                spawnX = playerTrapX,
                spawnLocation = spawnLocation,
            )
            self.enemyCount += 1
            enemyQueue.append(enemyCell)
            n += 1

        # cows
        n = 0
        while n < numCows:
            playerTrapX = waveIdx * intraWaveXoffset
            spawnLocation = self.getRandomSpawnCoords(rightSideBias=0.8)
            enemyCell = EnemyCell(
                id = self.enemyCount,
                characterType = CharacterType.cow,
                spawnTime = None,  # waveIdx * intraWaveSpawnTime,
                spawnX = playerTrapX,
                spawnLocation = spawnLocation,
            )
            self.enemyCount += 1
            enemyQueue.append(enemyCell)
            n += 1


    def spawnEnemy(self, enemyCell):
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


    def handlePosition(self, playerPosition, viewportX, numEnemiesAlive):
        # spawn more enemies?
        # note that will not spawn all enemies at a certain position at once,
        # but only on every move of the player
        if len(self.enemyQueue) == 0:
            return

        if numEnemiesAlive > self.maxEnemies:
            return

        enemyCell = self.enemyQueue[0]
        if enemyCell.spawnX < playerPosition.x:
            logger.info("Spawn: Pos: {}".format(playerPosition.x))
            self.spawnEnemy(enemyCell)
            self.enemySpawned.append(enemyCell)
            del self.enemyQueue[0]


    def handleTime(self):
        if len(self.enemyQueue) == 0:
            return

        # spawn more enemies?
        enemyCell = self.enemyQueue[0]
        if enemyCell.spawnTime is None:
            return

        if enemyCell.spawnTime < self.time:
            logger.info("Spawn: Time: {}".format(enemyCell.spawnTime))
            self.spawnEnemy(enemyCell)
            self.enemySpawned.append(enemyCell)
            del self.enemyQueue[0]


    def handleEnemyDeath(self):
        pass


    def advance(self, dt):
        self.time += dt


    def getRandomSpawnCoords(self, rightSideBias=0.5):
        # X
        myx = 0
        roll = random.random()
        if roll < rightSideBias:
            myx = self.viewport.getx() + Config.columns + 1
        else:
            myx = self.viewport.getx() - 1  # - enemy.texture.width

        # Y
        minY = Config.areaMoveable['miny']
        maxY = Config.areaMoveable['maxy']
        myy = random.randint(minY, maxY)

        spawnCoords = Coordinates(myx, myy)
        return spawnCoords
