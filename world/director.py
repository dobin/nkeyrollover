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
from entities.enemy.state_wander import StateWander

from system.advanceable import Advanceable
from system.renderable import Renderable
from system.gamelogic.attackable import Attackable
from system.gamelogic.tenemy import tEnemy

logger = logging.getLogger(__name__)


class Director(object):
    """Create and manage the enemies"""
    
    def __init__(self, viewport :Viewport, world):
        self.viewport = viewport
        self.world = world
        self.enemies = []
        self.lastEnemyResurrectedTimer = Timer(1.0)

        self.maxEnemies = 12
        self.maxEnemiesAttacking = 2
        self.maxEnemiesChasing = 4


    # we split this from the constructor, so we can initialize a Director 
    # without enemies in the unit test
    def init(self):
        if Config.devMode: 
            characterType = CharacterType.cow
            newEnemy = Enemy(viewport=self.viewport, 
                parent=self.world.worldSprite, 
                world=self.world, 
                name="Enym", 
                characterType=characterType)
            newEnemy.enemyMovement = Config.enemyMovement
            newEnemy.direction = Direction.right
            self.enemies.append(newEnemy)
            newEnemy.setActive(False)

            enemy = self.world.esperWorld.create_entity()
            self.world.esperWorld.add_component(enemy, Renderable(r=newEnemy))
            self.world.esperWorld.add_component(enemy, Advanceable(r=newEnemy))
            self.world.esperWorld.add_component(enemy, tEnemy(characterType=characterType))
            self.world.esperWorld.add_component(enemy, Attackable(initialHealth=100))

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
                self.enemies.append(newEnemy)
                newEnemy.setActive(False)

                enemy = self.world.esperWorld.create_entity()
                self.world.esperWorld.add_component(enemy, Renderable(r=newEnemy))
                self.world.esperWorld.add_component(enemy, Advanceable(r=newEnemy))
                self.world.esperWorld.add_component(enemy, tEnemy(characterType=characterType))
                self.world.esperWorld.add_component(enemy, Attackable(initialHealth=100))

                n += 1


    def numEnemiesAlive(self) -> int:
        n = 0
        for enemy in self.enemies:
            if enemy.isActive(): 
                n += 1
        return n


    def numEnemiesDead(self) -> int:
        n = 0
        for enemy in self.enemies:
            if not enemy.isActive(): 
                n += 1
        return n

    
    def numEnemiesAttacking(self) -> int:
        n = 0
        for enemy in self.enemies:
            if enemy.isActive():
                if enemy.brain.state.name == 'attack' or enemy.brain.state.name == 'attackwindup':
                    n += 1
        return n


    def numEnemiesWandering(self) -> int:
        n = 0
        for enemy in self.enemies:
            if enemy.isActive():
                if enemy.brain.state.name == 'wander':
                    n += 1
        return n


    def numEnemiesChasing(self) -> int:
        n = 0
        for enemy in self.enemies:
            if enemy.isActive():
                if enemy.brain.state.name == 'chase':
                    n += 1
        return n


    def canHaveMoreEnemiesAttacking(self) -> bool:
        n = self.numEnemiesAttacking()
        if n <= self.maxEnemiesAttacking:
            return True
        else: 
            return False

    
    def canHaveMoreEnemiesChasing(self) -> bool:
        n = self.numEnemiesChasing()
        if n <= self.maxEnemiesChasing:
            return True
        else: 
            return False


    def advanceEnemies(self, deltaTime):
        self.lastEnemyResurrectedTimer.advance(deltaTime)

        for enemy in self.enemies:
            if enemy.isActive():
                enemy.advance(deltaTime)


    def worldUpdate(self):
        # make more enemies
        if self.numEnemiesAlive() < self.maxEnemies:
            if self.lastEnemyResurrectedTimer.timeIsUp():
                self.lastEnemyResurrectedTimer.reset()
                
                if self.numEnemiesDead() > 0:
                    self.makeEnemyAlive()


    def findDeadEnemy(self): 
        for enemy in self.enemies:
            if not enemy.isActive():
                return enemy


    def makeEnemyAlive(self): 
        for ent, (attackable, renderable, enemy) in self.world.esperWorld.get_components(Attackable, Renderable, tEnemy):
            if renderable.r.brain.state.name == 'idle':
                logger.info("Ressurect enemy: " + str(renderable.r))
                attackable.resetHealth()
                spawnCoords = self.getRandomSpawnCoords(renderable.r)
                renderable.r.gmRessurectMe(spawncoord=spawnCoords)
                break


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
        for enemy in self.enemies:
            if enemy.isActive(): 
                if enemy.collidesWithPoint(characterWeaponCoordinates):
                    enemy.gmHandleHit(50)


    def getPlayersHit(self, coordinates):
        players = []
        if self.world.getPlayer().collidesWithPoint(coordinates):
            players.append(self.world.getPlayer())

        return players

