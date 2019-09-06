import esper
import random

from system.gamelogic.enemy import Enemy
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


class EnemyProcessor(esper.Processor):
    def __init__(self, viewport):
        super().__init__()
        self.viewport = viewport


    def process(self, deltaTime):
        for ent, player in self.world.get_component(Enemy):
            player.advance(deltaTime)
        self.checkSpawn()

    
    def checkSpawn(self):
        for message in messaging.getByType(MessageType.SpawnEnemy):
            self.spawnEnemy(message.data)


    def spawnEnemy(self, message):
        id = message.id
        characterType = message.characterType
        coordinates = message.spawnLocation

        name = "Bot " + str(id)
        # Enemy
        groupId = GroupId(id=id)
        enemy = self.world.create_entity()
        esperData = EsperData(self.world, enemy, name)
        texture = CharacterTexture(
            characterAnimationType=CharacterAnimationType.standing,
            head=self.getRandomHead(),
            body=self.getRandomBody(),
            characterType=characterType)
        texture.name = name
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates,
            active=True)
        renderable.name = name
        renderable.world = self.world
        renderable.enemyMovement = True
        self.world.add_component(enemy, groupId)
        self.world.add_component(enemy, renderable)
        tenemy = Enemy(
            name=name,
            world=self.world)
        ai = Ai(
            name=name,
            esperData=esperData)
        self.world.add_component(enemy, ai)

        self.world.add_component(enemy, tenemy)
        self.world.add_component(enemy, Attackable(initialHealth=100))
        enemyRenderable = renderable
        # /Enemy

        # CharacterAttack
        characterAttackEntity = self.world.create_entity()
        texture :PhenomenaTexture = PhenomenaTexture(
            phenomenaType=PhenomenaType.hit)
        texture.name = "EnemyWeapon " + name
        coordinates = Coordinates( # for hit
            0,
            0
        )
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=enemyRenderable,
            coordinates=coordinates,
            z=2,
            useParentDirection=True,
            active=False)
        renderable.setLocation(
           Coordinates(-1 * (renderable.texture.width - 2), 1)
        )
        renderable.name = "EnemyWeapon " + name
        texture.parentSprite = renderable
        self.world.add_component(characterAttackEntity, renderable)
        offensiveAttack = OffensiveAttack(
            isPlayer=False,
            world=self.world,
            renderable=renderable)
        self.world.add_component(characterAttackEntity, groupId)
        self.world.add_component(characterAttackEntity, offensiveAttack)
        self.characterAttackEntity = characterAttackEntity
        offensiveAttack.switchWeapon(WeaponType.hitLine)
        tenemy.offensiveAttackEntity = characterAttackEntity
        # /CharacterAttack


    def getRandomHead(self):
        return random.choice([ '^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self):
        return random.choice([ 'X', 'o', 'O', 'v', 'V', 'M', 'm' ])
