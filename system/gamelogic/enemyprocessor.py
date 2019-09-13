import esper
import random
import logging

from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexture import CharacterTexture
from game.enemytype import EnemyType
from system.groupid import GroupId
from system.graphics.renderable import Renderable
from system.gamelogic.enemy import Enemy
from system.gamelogic.attackable import Attackable
from system.gamelogic.esperdata import EsperData
from system.gamelogic.ai import Ai
from system.gamelogic.offensiveattack import OffensiveAttack
from system.gamelogic.weapontype import WeaponType
from messaging import messaging, MessageType
import game.uniqueid

logger = logging.getLogger(__name__)


class EnemyProcessor(esper.Processor):
    def __init__(self, viewport, enemyLoader):
        super().__init__()
        self.enemyLoader = enemyLoader
        self.viewport = viewport


    def process(self, deltaTime):
        for ent, player in self.world.get_component(Enemy):
            player.advance(deltaTime)

        self.checkSpawn()


    def checkSpawn(self):
        for message in messaging.getByType(MessageType.SpawnEnemy):
            self.spawnEnemy(message.data)


    def spawnEnemy(self, data):
        id = game.uniqueid.getUniqueId()
        enemyType = data.enemyType
        coordinates = data.spawnLocation

        enemySeed = self.enemyLoader.getSeedForEnemy(enemyType)

        name = "Bot " + str(id)
        groupId = GroupId(id=id)
        enemy = self.world.create_entity()
        esperData = EsperData(self.world, enemy, name)
        tenemy = Enemy(name=name, enemyInfo=enemySeed.enemyInfo)
        attackable = Attackable(initialHealth=enemySeed.health)
        ai = Ai(
            name=name,
            esperData=esperData,
            enemyType=enemyType)

        texture = CharacterTexture(
            characterAnimationType=CharacterAnimationType.standing,
            head=self.getRandomHead(),
            body=self.getRandomBody(),
            characterTextureType=enemySeed.characterTextureType,
            name=name)

        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates,
            active=True,
            name=name)

        offensiveAttack = OffensiveAttack(
            parentChar=tenemy,
            parentRenderable=renderable)
        offensiveAttack.switchWeapon(enemySeed.weaponType)

        self.world.add_component(enemy, ai)
        self.world.add_component(enemy, groupId)
        self.world.add_component(enemy, renderable)
        self.world.add_component(enemy, tenemy)
        self.world.add_component(enemy, attackable)
        self.world.add_component(enemy, offensiveAttack)


    def getRandomHead(self):
        return random.choice(['^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self):
        return random.choice(['X', 'o', 'O', 'v', 'V', 'M', 'm'])
