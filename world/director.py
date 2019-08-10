import logging

from entities.enemy.enemy import Enemy
from utilities.timer import Timer
from config import Config

logger = logging.getLogger(__name__)


class Director(object):
    """Create and manage the enemies"""
    
    def __init__(self, viewport, world):
        self.viewport = viewport
        self.world = world
        self.enemiesDead = []
        self.enemiesAlive = []
        self.lastEnemyResurrectedTimer = Timer(1.0)

        self.maxEnemies = 12

    # we split this from the constructor, so we can initialize a Director 
    # without enemies in the unit test
    def init(self):

        if Config.devMode: 
            coordinates = {
                'x': 30, 
                'min_y': 13,
                'max_y': 13,
            }
            newEnemy = Enemy(viewport=self.viewport, 
                parent=self.world.worldSprite, 
                spawnBoundaries=coordinates, 
                world=self.world, 
                name="Enym")
            newEnemy.enemyMovement = False
            self.enemiesDead.append(newEnemy)
        else:
            n = 0
            maxN = self.maxEnemies
            if Config.devMode:
                maxN = 1
            while n < maxN:
                myx = 1
                if n % 2 == 0:
                    myx = Config.columns + 1

                coordinates = {
                    'x': myx, 
                    'min_y': Config.areaMoveable['miny'],
                    'max_y': Config.areaMoveable['maxy'],
                }
                newEnemy = Enemy(viewport=self.viewport, 
                    parent=self.world.worldSprite, 
                    spawnBoundaries=coordinates, 
                    world=self.world, 
                    name=str(n))
                self.enemiesDead.append(newEnemy)
                n = n + 1


    def advanceEnemies(self, deltaTime):
        self.lastEnemyResurrectedTimer.advance(deltaTime)
        
        for enemy in self.enemiesAlive:
            enemy.advance(deltaTime)


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
                logger.info("Ressurect, alive: " + str(len(self.enemiesAlive)))
                enemy = self.enemiesDead.pop()
                enemy.gmRessurectMe()
                self.enemiesAlive.append(enemy)

        # remove inactive enemies
        for enemy in self.enemiesAlive:
            if not enemy.isActive():
                logger.info("Move newly dead enemy to dead queue")
                self.enemiesDead.append(enemy)
                self.enemiesAlive.remove(enemy)


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

