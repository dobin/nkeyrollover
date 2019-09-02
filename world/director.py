import logging
import random

from utilities.timer import Timer
from config import Config
from world.viewport import Viewport
#from world.world import World
from sprite.direction import Direction
from texture.character.charactertype import CharacterType
from sprite.coordinates import Coordinates
from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexture import CharacterTexture
from texture.texture import Texture
from entities.weapontype import WeaponType

from system.groupid import GroupId
from system.advanceable import Advanceable
from system.renderable import Renderable
from system.gamelogic.attackable import Attackable
from system.gamelogic.enemy import Enemy
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from system.offensiveattack import OffensiveAttack
from messaging import messaging, Messaging, Message, MessageType
from entities.esperdata import EsperData
from system.gamelogic.ai import Ai

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
            self.createEnemy(characterType, 0)
        else:
            n = 0
            while n < self.maxEnemies:
                characterType = CharacterType.stickfigure
                if n % 10 == 0:
                    characterType = CharacterType.cow
                self.createEnemy(characterType, n)
                n += 1


    def createEnemy(self, characterType, id):
        name = "Bot " + str(id)
        # Enemy
        groupId = GroupId(id=id)
        enemy = self.world.esperWorld.create_entity()
        esperData = EsperData(self.world.esperWorld, enemy, name)
        texture = CharacterTexture(
            characterAnimationType=CharacterAnimationType.standing,
            head=self.getRandomHead(),
            body=self.getRandomBody(),
            characterType=characterType)
        coordinates = Coordinates(0, 0)
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates,
            active=False)
        renderable.name = "Enemy "
        renderable.world = self.world
        renderable.enemyMovement = True
        self.world.esperWorld.add_component(enemy, groupId)
        self.world.esperWorld.add_component(enemy, renderable)
        tenemy = Enemy(
            player=self.world.playerRendable,
            name=name,
            world=self.world,
            viewport=self.viewport)
        ai = Ai(
            name=name,
            esperData=esperData,
            director=self)
        self.world.esperWorld.add_component(enemy, ai)

        self.world.esperWorld.add_component(enemy, tenemy)
        self.enemies.append(ai)
        self.world.esperWorld.add_component(enemy, Attackable(initialHealth=100))
        enemyRenderable = renderable
        # /Enemy

        # CharacterAttack
        characterAttackEntity = self.world.esperWorld.create_entity()
        texture :PhenomenaTexture = PhenomenaTexture(
            phenomenaType=PhenomenaType.hit)
        coordinates = Coordinates( # for hit
            -1,
            1
        )
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=enemyRenderable,
            coordinates=coordinates,
            z=2,
            useParentDirection=True)
        renderable.name = "EnemyWeapon "
        texture.parentSprite = renderable
        self.world.esperWorld.add_component(characterAttackEntity, renderable)
        offensiveAttack = OffensiveAttack(
            isPlayer=False,
            world=self.world,
            renderable=renderable)
        self.world.esperWorld.add_component(characterAttackEntity, groupId)
        self.world.esperWorld.add_component(characterAttackEntity, offensiveAttack)
        self.characterAttackEntity = characterAttackEntity
        offensiveAttack.switchWeapon(WeaponType.hitLine)
        tenemy.offensiveAttackEntity = characterAttackEntity
        # /CharacterAttack


    def getRandomHead(self):
        return random.choice([ '^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self):
        return random.choice([ 'X', 'o', 'O', 'v', 'V', 'M', 'm' ])


    def numEnemiesAlive(self) -> int:
        n = 0
        for enemy in self.enemies:
            if enemy.brain.state.name != 'idle':
                n += 1
        return n


    def numEnemiesDead(self) -> int:
        n = 0
        for enemy in self.enemies:
            if enemy.brain.state.name == 'idle':
                n += 1
        return n


    def numEnemiesAttacking(self) -> int:
        n = 0
        for enemy in self.enemies:
            #if enemy.isActive():
            if enemy.brain.state.name == 'attack' or enemy.brain.state.name == 'attackwindup':
                n += 1
        return n


    def numEnemiesWandering(self) -> int:
        n = 0
        for enemy in self.enemies:
            #if enemy.isActive():
            if enemy.brain.state.name == 'wander':
                n += 1
        return n


    def numEnemiesChasing(self) -> int:
        n = 0
        for enemy in self.enemies:
            #if enemy.isActive():
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


    def advance(self, deltaTime):
        self.lastEnemyResurrectedTimer.advance(deltaTime)


    def worldUpdate(self):
        # make more enemies
        if self.numEnemiesAlive() < self.maxEnemies:
            if self.lastEnemyResurrectedTimer.timeIsUp():
                if self.numEnemiesDead() > 0:
                    self.makeEnemyAlive()
                    self.lastEnemyResurrectedTimer.reset()


    def findDeadEnemy(self):
        for enemy in self.enemies:
            if not enemy.isActive():
                return enemy


    def makeEnemyAlive(self):
        for ent, (attackable, ai, renderable, enemy) in self.world.esperWorld.get_components(
            Attackable, Ai, Renderable, Enemy
        ):
            logging.info("Make enemy alive")
            if ai.brain.state.name == 'idle':
                spawnCoords = self.getRandomSpawnCoords(renderable)
                renderable.setLocation(spawnCoords)

                logger.info("Ressurect enemy {} at {}".format(enemy, renderable.coordinates))
                attackable.resetHealth()

                ai.brain.pop()
                ai.brain.push('spawn')

                # if death animation was deluxe, there is no frame in the sprite
                # upon spawning, and an exception is thrown
                # change following when fixed TODO
                renderable.texture.changeAnimation(
                    CharacterAnimationType.standing,
                    renderable.direction)
                renderable.setActive(True)

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