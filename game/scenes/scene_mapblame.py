import logging
import random

from game.scenes.scenebase import SceneBase
from common.coordinates import Coordinates
from messaging import messaging, MessageType
from collections import deque
from config import Config
from game.enemytype import EnemyType
from utilities.entityfinder import EntityFinder
import system.groupid
from directmessaging import directMessaging, DirectMessageType
from common.direction import Direction

logger = logging.getLogger(__name__)


class EnemyCell(object):
    def __init__(self, id, enemyType, spawnTime, spawnX, spawnLocation, spawnDirection):
        self.id = id
        self.enemyType = enemyType
        self.spawnTime = spawnTime
        self.spawnX = spawnX

        self.spawnDirection = spawnDirection  # spawn left/right of current viewport
        self.spawnLocation = spawnLocation  # spawn at this position


    def __repr__(self):
        return "{} {} @{} @{} @{}".format(
            self.id,
            self.enemyType,
            self.spawnTime,
            self.spawnX,
            self.spawnLocation)


class Akt(object):
    def __init__(self):
        self.min_x = 0
        self.max_x = 0
        self.enemyQueue = deque()


class SceneMapBlame(SceneBase):
    def __init__(self, viewport, world):
        super().__init__(world=world, viewport=viewport)
        self.name = "Scene2"
        self.isShowPlayer = True
        self.isShowMap = True

        self.enemyQueue = deque()

        self.maxEnemies = 6
        self.time = 0.0
        self.enemyCount = 0

        self.prepareEnemies()
        self.speechBubbles = [
            {
                'timeSpawn': 1.0,
                'timeShow': 1.0,
                'text': 'I am here to chew game and kick ass'
            },
            {
                'timeSpawn': 2.5,
                'timeShow': 1.0,
                'text': 'And I am all out of gum'
            },
        ]


    def prepareEnemies(self):
        if Config.devMode:
            enemyCell = EnemyCell(
                id = self.enemyCount,
                enemyType = EnemyType.stickfigure,
                spawnTime = None,
                spawnX = 0,
                spawnLocation = Coordinates(35, 8),
                spawnDirection = None
            )
            self.enemyQueue.append(enemyCell)

            enemyCell = EnemyCell(
                id = self.enemyCount,
                enemyType = EnemyType.cow,
                spawnTime = None,
                spawnX = 40,
                spawnLocation = Coordinates(85, 13),
                spawnDirection = None
            )
            self.enemyQueue.append(enemyCell)

            enemyCell = EnemyCell(
                id = self.enemyCount,
                enemyType = EnemyType.stickfigure,
                spawnTime = None,
                spawnX = 80,
                spawnLocation = Coordinates(60 + 80, 13),
                spawnDirection = None
            )
            self.enemyQueue.append(enemyCell)
            return

        waveIdx = 0
        waveCount = 9
        while waveIdx < waveCount:
            self.prepareWave(waveIdx, self.enemyQueue)
            waveIdx += 1


    def prepareWave(self, waveIdx, enemyQueue):
        # intraWaveSpawnTime = 3
        intraWaveXoffset = 50

        numStickfigures = 10
        numCows = 2
        numDragons = 1

        n = 0
        while n < numStickfigures:
            playerTrapX = waveIdx * intraWaveXoffset
            # spawnLocation = self.getRandomSpawnCoords(
            #    trapX=playerTrapX, rightSideBias=0.8)

            dir = Direction.left
            roll = random.random()
            if roll < 0.8:
                dir = Direction.right

            enemyCell = EnemyCell(
                id = self.enemyCount,
                enemyType = EnemyType.stickfigure,
                spawnTime = None,  # waveIdx * intraWaveSpawnTime + n,
                spawnX = playerTrapX,
                spawnLocation = None,
                spawnDirection = dir
            )
            self.enemyCount += 1
            enemyQueue.append(enemyCell)
            n += 1

        n = 0
        while n < numCows:
            playerTrapX = waveIdx * intraWaveXoffset
            # spawnLocation = self.getRandomSpawnCoords(
            #    trapX=playerTrapX, rightSideBias=0.8)
            enemyCell = EnemyCell(
                id = self.enemyCount,
                enemyType = EnemyType.cow,
                spawnTime = None,  # waveIdx * intraWaveSpawnTime,
                spawnX = playerTrapX,
                spawnLocation = None,
                spawnDirection = None,
            )
            self.enemyCount += 1
            enemyQueue.append(enemyCell)
            n += 1

        n = 0
        while n < numDragons:
            playerTrapX = waveIdx * intraWaveXoffset
            # spawnLocation = self.getRandomSpawnCoords(
            #    trapX=playerTrapX, rightSideBias=0.8)
            enemyCell = EnemyCell(
                id = self.enemyCount,
                enemyType = EnemyType.dragon,
                spawnTime = None,  # waveIdx * intraWaveSpawnTime,
                spawnX = playerTrapX,
                spawnLocation = None,
                spawnDirection = None,
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

        enemyCell = self.getNextEnemy()
        if enemyCell.spawnX < playerPosition.x:
            logger.info("Spawn: Pos: {}".format(playerPosition.x))
            self.spawnEnemy(enemyCell)
            self.enemyQueue.remove(enemyCell)


    def getNextEnemy(self):
        return self.enemyQueue[0]


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
            del self.enemyQueue[0]


    def handleEnemyDeath(self):
        pass


    def advance(self, dt):
        self.time += dt

        if len(self.speechBubbles) > 0:
            speechEntry = self.speechBubbles[0]
            if self.time > speechEntry['timeSpawn']:
                playerEnt = EntityFinder.findPlayer(self.world)
                playerGroupId = self.world.component_for_entity(
                    playerEnt, system.groupid.GroupId)

                directMessaging.add(
                    groupId = playerGroupId.getId(),
                    type = DirectMessageType.activateSpeechBubble,
                    data = {
                        'text': speechEntry['text'],
                        'time': speechEntry['timeShow'],
                        'waitTime': 0,
                    }
                )
                self.speechBubbles.pop(0)


    def getRandomSpawnCoords(self, trapX, rightSideBias=0.5):
        # X
        myx = 0
        roll = random.random()
        if roll < rightSideBias:
            myx = trapX + Config.columns + 1
        else:
            myx = trapX - 1 - 5  # - enemy.texture.width

        # Y
        minY = Config.areaMoveable['miny']
        maxY = Config.areaMoveable['maxy']
        myy = random.randint(minY, maxY)

        spawnCoords = Coordinates(myx, myy)
        return spawnCoords