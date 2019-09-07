import esper
import random
import logging

from system.gamelogic.enemy import Enemy
from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexture import CharacterTexture
from system.groupid import GroupId
from system.graphics.renderable import Renderable

from system.gamelogic.attackable import Attackable
from messaging import messaging, MessageType
from entities.esperdata import EsperData
from system.gamelogic.ai import Ai
import world.uniqueid
from system.gamelogic.offensiveattack import OffensiveAttack

logger = logging.getLogger(__name__)


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
        id = world.uniqueid.getUniqueId()
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
        tenemy = Enemy(name=name)
        ai = Ai(
            name=name,
            esperData=esperData)
        self.world.add_component(enemy, ai)

        self.world.add_component(enemy, tenemy)
        self.world.add_component(enemy, Attackable(initialHealth=100))

        offensiveAttack = OffensiveAttack(
            parentChar=tenemy,
            parentRenderable=renderable)
        self.world.add_component(enemy, offensiveAttack)


    def getRandomHead(self):
        return random.choice(['^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self):
        return random.choice(['X', 'o', 'O', 'v', 'V', 'M', 'm'])
