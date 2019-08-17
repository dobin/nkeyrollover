import logging
import random

from entities.enemy.enemy import Enemy
from utilities.timer import Timer
from config import Config
from world.viewport import Viewport
#from world.world import World
from sprite.direction import Direction
from texture.character.charactertype import CharacterType
from sprite.coordinates import Coordinates
from entities.enemy.state_attack import StateAttack
from entities.enemy.state_attackwindup import StateAttackWindup
from entities.enemy.state_chase import StateChase

logger = logging.getLogger(__name__)


class Director(object):
    """Create and manage the enemies"""
    
    def __init__(self, viewport :Viewport, world):
        self.viewport = viewport
        self.world = world
        self.enemiesDead = []
        # sorted by increasing enemy.coordinates.y order after every advance()
        # to have a good Z order on screen
        self.enemiesAlive = [] 
        self.lastEnemyResurrectedTimer = Timer(1.0)

        self.maxEnemies = 12
        self.maxEnemiesAttacking = 2
        self.maxEnemiesChasing = 4


    # we split this from the constructor, so we can initialize a Director 
    # without enemies in the unit test
    def init(self):
        if Config.devMode: 
            newEnemy = Enemy(viewport=self.viewport, 
                parent=self.world.worldSprite, 
                world=self.world, 
                name="Enym", 
                characterType=CharacterType.cow)
            newEnemy.enemyMovement = Config.enemyMovement
            newEnemy.direction = Direction.right
            self.enemiesDead.append(newEnemy)
        else:
            n = 0
            while n < self.maxEnemies:
                characterType = CharacterType.stickfigure
                if n % 10 == 0:
                    characterType = CharacterType.cow

                newEnemy = Enemy(viewport=self.viewport, 
                    parent=self.world.worldSprite, 
                    world=self.world, 
                    name=str(n),
                    characterType=characterType)
                self.enemiesDead.append(newEnemy)
                n = n + 1

    
    def canHaveMoreEnemiesAttacking(self) -> bool:
        n = 0
        for enemy in self.enemiesAlive:
            if enemy.brain.state == StateAttack or enemy.brain.state == StateAttackWindup:
                n += 1

        if n <= self.maxEnemiesAttacking:
            return True
        else: 
            return False

    
    def canHaveMoreEnemiesChasing(self) -> bool:
        n = 0
        for enemy in self.enemiesAlive:
            if enemy.brain.state == StateChase:
                n += 1

        if n <= self.maxEnemiesChasing:
            return True
        else: 
            return False


    def advanceEnemies(self, deltaTime):
        self.lastEnemyResurrectedTimer.advance(deltaTime)

        for enemy in self.enemiesAlive:
            enemy.advance(deltaTime)

        def gety(elem): 
            return elem.coordinates.y
        self.enemiesAlive.sort(key=gety)            


    def drawEnemies(self):
        for enemy in self.enemiesAlive: 
            enemy.draw()


    def drawEnemyAttacks(self): 
        for enemy in self.enemiesAlive: 
            enemy.drawCharacterAttack()


    def worldUpdate(self):
        # make more enemies
        if len(self.enemiesAlive) < self.maxEnemies:
            if self.lastEnemyResurrectedTimer.timeIsUp():
                self.lastEnemyResurrectedTimer.reset()
                
                if len(self.enemiesDead) > 0:
                    logger.warn("Ressurect an enemy. alive are: " + str(len(self.enemiesAlive)))
                    enemy = self.enemiesDead.pop()
                    spawnCoords = self.getRandomSpawnCoords(enemy)
                    enemy.gmRessurectMe(spawnCoords)
                    self.enemiesAlive.append(enemy)

        # remove inactive enemies
        for enemy in self.enemiesAlive:
            if not enemy.isActive():
                logger.info("Move newly dead enemy to dead queue")
                self.enemiesDead.append(enemy)
                self.enemiesAlive.remove(enemy)


    def getRandomSpawnCoords(self, enemy):
        if Config.devMode: 
            coordinates = Coordinates(
                x=40, 
                y=15,
            )
            return coordinates

        side = random.choice([True, False])
        myx = 0
        if side: 
            myx = self.viewport.getx() + Config.columns + 1
        else: 
            myx = self.viewport.getx() - 1 - enemy.texture.width

        minY = Config.areaMoveable['miny']
        maxY = Config.areaMoveable['maxy']
        myy = random.randint(minY, maxY)
        spawnCoords = Coordinates(myx, myy)
        return spawnCoords


    def collisionDetection(self, characterWeaponCoordinates): 
        for enemy in self.enemiesAlive: 
            if enemy.collidesWithPoint(characterWeaponCoordinates):
                enemy.gmHandleHit(50)


    def getEnemiesHit(self, coordinates):
        enemies = []
        for enemy in self.enemiesAlive: 
            if enemy.collidesWithPoint(coordinates):
                enemies.append(enemy)

        return enemies


    def getPlayersHit(self, coordinates):
        players = []
        if self.world.player.collidesWithPoint(coordinates):
            players.append(self.world.player)

        return players

