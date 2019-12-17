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
from .enemycell import EnemyCell

logger = logging.getLogger(__name__)


class Akt(object):
    def __init__(self):
        self.min_x = 0
        self.max_x = 0
        self.enemyQueue = deque()


class SceneMapBlame(SceneBase):
    def __init__(self, viewport, world):
        super().__init__(world=world, viewport=viewport, hasEnvironment=True)
        self.name = "MapBlame"
        self.isShowPlayer = True
        self.isShowMap = True
        self.enemyQueue = None
        self.maxEnemies = 6
        self.enemyCount = 0

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
        if Config.devMode:
            self.speechBubbles = []

        self.init()


    def init(self):
        self.time = 0.0
        self.enemyQueue = deque()  # note: Important that this is in init()
        self.prepareEnemies()


    def prepareDebugEnemies(self):
        enemyCell = EnemyCell(
            id = self.enemyCount,
            enemyType = EnemyType.rambo,
            spawnTime = None,
            spawnX = 25,
            spawnLocation = Coordinates(36, 8),
            spawnDirection = None
        )
        self.enemyQueue.append(enemyCell)

        enemyCell = EnemyCell(
            id = self.enemyCount,
            enemyType = EnemyType.stickfigure,
            spawnTime = None,
            spawnX = 50,
            spawnLocation = Coordinates(50, 8),
            spawnDirection = None
        )
        self.enemyQueue.append(enemyCell)

        enemyCell = EnemyCell(
            id = self.enemyCount,
            enemyType = EnemyType.cow,
            spawnTime = None,
            spawnX = 45,
            spawnLocation = Coordinates(86, 13),
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


    def prepareEnemies(self):
        if Config.devMode:
            self.prepareDebugEnemies()

        waveIdx = 0
        waveCount = 9

        intraWaveXoffset = 30
        waveX = 30
        while waveIdx < waveCount:
            self.prepareWave(waveX, self.enemyQueue)
            waveIdx += 1
            waveX += intraWaveXoffset


    def prepareWave(self, waveX, enemyQueue):
        # intraWaveSpawnTime = 3

        numStickfigures = 5
        numCows = 2
        numDragons = 1
        numRambos = 2
        numBig = 2

        n = 0
        while n < numStickfigures:
            playerTrapX = waveX
            # spawnLocation = self.getRandomSpawnCoords(
            #    trapX=playerTrapX, rightSideBias=0.8)

            xoff = random.randint(0, 4)
            roll = random.random()
            if roll < 0.8:
                dir = Direction.right
                playerTrapX += xoff
            else:
                dir = Direction.left
                playerTrapX -= xoff

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
        while n < numBig:
            playerTrapX = waveX
            # spawnLocation = self.getRandomSpawnCoords(
            #    trapX=playerTrapX, rightSideBias=0.8)

            xoff = random.randint(0, 4)
            roll = random.random()
            if roll < 0.8:
                dir = Direction.right
                playerTrapX += xoff
            else:
                dir = Direction.left
                playerTrapX -= xoff

            enemyCell = EnemyCell(
                id = self.enemyCount,
                enemyType = EnemyType.big,
                spawnTime = None,  # waveIdx * intraWaveSpawnTime + n,
                spawnX = playerTrapX,
                spawnLocation = None,
                spawnDirection = dir
            )
            self.enemyCount += 1
            enemyQueue.append(enemyCell)
            n += 1

        n = 0
        while n < numRambos:
            playerTrapX = waveX
            # spawnLocation = self.getRandomSpawnCoords(
            #    trapX=playerTrapX, rightSideBias=0.8)

            xoff = random.randint(0, 4)
            roll = random.random()
            if True:  # always on the right
                dir = Direction.right
                playerTrapX += xoff
            else:
                dir = Direction.left
                playerTrapX -= xoff

            enemyCell = EnemyCell(
                id = self.enemyCount,
                enemyType = EnemyType.rambo,
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
            xoff = random.randint(0, 4)
            playerTrapX = waveX + 10 + xoff
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
            playerTrapX = waveX + 30
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
        if enemyCell.spawnX % 2 != 0:
            logger.warning("Spawn enemy at uneven location!")

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
