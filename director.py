from enemy.enemy import Enemy
import logging

logger = logging.getLogger(__name__)
from config import Config

class Director(object):
    def __init__(self, win):
        self.win = win
        self.enemiesDead = []
        self.enemiesAlive = []
        self.lastEnemyResurrectedTime = 0
        self.enemyRessuractionTime = Config.secToFrames(1)
        self.maxEnemies = 5

        n = 0
        while n < 16:
            data = {
                'min_x': 30, 
                'min_y': 10,
                'max_x': Config.columns - 5,
                'max_y': Config.rows - 5
            }
            newEnemy = Enemy(self.win, data)
            self.enemiesDead.append(newEnemy)
            n = n + 1


    def advanceEnemies(self):
        self.lastEnemyResurrectedTime += 1
        
        for enemy in self.enemiesAlive:
            enemy.advance()


    def drawEnemies(self):
        for enemy in self.enemiesAlive: 
            enemy.draw()


    def worldUpdate(self): 
        # make more enemies
        if len(self.enemiesAlive) < self.maxEnemies:
            if self.lastEnemyResurrectedTime > self.enemyRessuractionTime:
                self.lastEnemyResurrectedTime = 0
                logger.warning("Ressurect, alive: " + str(len(self.enemiesAlive)))
                enemy = self.enemiesDead.pop()
                enemy.ressurectMe()
                self.enemiesAlive.append(enemy)


    def collisionDetection(self, playerHitCoordinates): 
        for enemy in self.enemiesAlive: 
            if enemy.collidesWithPoint(playerHitCoordinates):
                enemy.getHit(50)

                if not enemy.playerStatus.isAlive():
                    logger.warning("Move newly dead enemy to dead queue")
                    self.enemiesDead.append(enemy)
                    self.enemiesAlive.remove(enemy)
