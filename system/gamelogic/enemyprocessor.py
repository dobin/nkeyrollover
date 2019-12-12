import esper
import logging
import random

from texture.character.charactertexture import CharacterTexture
from system.groupid import GroupId
from system.graphics.renderable import Renderable
from system.gamelogic.enemy import Enemy
from system.gamelogic.attackable import Attackable
from system.gamelogic.esperdata import EsperData
from system.gamelogic.ai import Ai
from system.gamelogic.offensiveattack import OffensiveAttack
from system.graphics.physics import Physics
from messaging import messaging, MessageType
import game.uniqueid
from common.coordinates import Coordinates, ExtCoordinates
from utilities.entityfinder import EntityFinder
from utilities.objectcache import ObjectCache
from config import Config
from common.direction import Direction
from texture.character.characteranimationtype import CharacterAnimationType
from game.enemyloader import EnemyLoader


logger = logging.getLogger(__name__)


class EnemyCached(object):
    def __init__(self):
        self.physics = None
        self.ai = None
        self.groupId = None
        self.renderable = None
        self.tenemy = None
        self.attackable = None
        self.offensiveAttack = None


class EnemyProcessor(esper.Processor):
    def __init__(self, viewport):
        super().__init__()
        self.enemyLoader :EnemyLoader = EnemyLoader()
        self.viewport = viewport
        self.num = 64
        self.objectCache = ObjectCache(size=self.num)
        self.didLoad = False


    def init(self):
        n = 0
        while n < self.num:
            enemyCached = self.createEnemyCached()
            self.objectCache.addObject(enemyCached)
            n += 1


    def process(self, deltaTime):
        # workaround, because we dont have self.world in __init__()...
        if not self.didLoad:
            self.init()
            self.didLoad = True

        for ent, player in self.world.get_component(Enemy):
            player.advance(deltaTime)

        self.checkSpawn()
        self.checkDead()


    def checkSpawn(self):
        for message in messaging.getByType(MessageType.SpawnEnemy):
            self.spawnEnemy(message.data)


    def checkDead(self):
        for ent, (ai, enemy) in self.world.get_components(Ai, Enemy):
            # remove enemies which are completely dead
            if ai.brain.state.name == 'dead':
                # first, add it again to the cache
                renderable = self.world.component_for_entity(ent, Renderable)
                groupId = self.world.component_for_entity(ent, GroupId)
                attackable = self.world.component_for_entity(ent, Attackable)
                offensiveAttack = self.world.component_for_entity(ent, OffensiveAttack)
                enemyCached = EnemyCached()
                enemyCached.groupId = groupId
                enemyCached.renderable = renderable
                enemyCached.tenemy = enemy
                enemyCached.attackable = attackable
                enemyCached.offensiveAttack = offensiveAttack
                self.objectCache.addObject(enemyCached)

                # delete it
                logger.info("Remove Entity G: {}".format(ent))
                self.world.delete_entity(ent)

                # message everyone that it is really dead now
                messaging.add(
                    type = MessageType.EntityDead,
                    groupId = None,
                    data = {}
                )

    def setSomeSpawnCoordinates(self, renderable, direction):
        # X
        if direction is Direction.right:
            myx = self.viewport.getx() + Config.columns + 1
        else:
            myx = self.viewport.getx() - 1 - renderable.texture.width

        minY = Config.areaMoveable['miny']
        maxY = Config.areaMoveable['maxy']
        myy = random.randint(minY, maxY)

        renderable.setLocation(Coordinates(myx, myy))

        # if enemies overlap, move them sideway away from player
        spotFree = False
        while not spotFree:
            if EntityFinder.isDestinationEmpty(
                world=self.world, renderable=renderable
            ):
                spotFree = True
            else:
                if direction is Direction.right:
                    renderable.coordinates.x += 3
                else:
                    renderable.coordinates.x -= 3


    def spawnEnemy(self, data):
        enemyType = data.enemyType
        coordinates = data.spawnLocation
        enemyCached = self.objectCache.getObject()
        enemySeed = self.enemyLoader.getSeedForEnemy(enemyType)

        entity = self.world.create_entity()
        esperData = EsperData(self.world, entity, enemyCached.renderable.name)  # ugly

        enemyCached.tenemy.setEnemyInfo(enemySeed.enemyInfo)
        enemyCached.attackable.setHealth(enemySeed.health)
        enemyCached.attackable.setMaxStunCount(enemySeed.stunCount)
        enemyCached.attackable.setStunTime(enemySeed.stunTime)
        enemyCached.attackable.setStunTimeFrame(enemySeed.stunTimeFrame)
        enemyCached.attackable.setKnockdownChance(enemySeed.knockdownChance)
        enemyCached.attackable.setKnockbackChance(enemySeed.knockbackChance)
        enemyCached.ai.setEnemyType(enemyType)
        enemyCached.ai.initAi(esperData=esperData)
        enemyCached.renderable.texture.setCharacterTextureType(
            enemySeed.characterTextureType)
        enemyCached.renderable.texture.changeAnimation(
            CharacterAnimationType.standing,
            enemyCached.renderable.direction)
        enemyCached.renderable.setActive(True)

        # after texture config above
        if coordinates is None:
            self.setSomeSpawnCoordinates(
                enemyCached.renderable,
                data.spawnDirection)
        else:
            enemyCached.renderable.setLocation(coordinates)

        enemyCached.renderable.attackBaseLocation = Coordinates(
            enemySeed.attackBaseLocation['x'],
            enemySeed.attackBaseLocation['y']
        )
        enemyCached.offensiveAttack.switchWeapon(enemySeed.weaponType)

        self.world.add_component(entity, enemyCached.physics)
        self.world.add_component(entity, enemyCached.ai)
        self.world.add_component(entity, enemyCached.groupId)
        self.world.add_component(entity, enemyCached.renderable)
        self.world.add_component(entity, enemyCached.tenemy)
        self.world.add_component(entity, enemyCached.attackable)
        self.world.add_component(entity, enemyCached.offensiveAttack)


    def createEnemyCached(self):
        id = game.uniqueid.getUniqueId()
        name = "Bot " + str(id)
        groupId = GroupId(id=id)
        tenemy = Enemy(name=name)
        attackable = Attackable()
        ai = Ai(name=name)
        texture = CharacterTexture(
            name=name)
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            active=True,
            name=name)
        offensiveAttack = OffensiveAttack(
            parentChar=tenemy,
            parentRenderable=renderable)
        physics = Physics()

        enemyCached = EnemyCached()
        enemyCached.ai = ai
        enemyCached.groupId = groupId
        enemyCached.renderable = renderable
        enemyCached.tenemy = tenemy
        enemyCached.attackable = attackable
        enemyCached.offensiveAttack = offensiveAttack
        enemyCached.physics = physics
        return enemyCached
