import esper
import random
import logging

from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexture import CharacterTexture
from texture.character.charactertype import CharacterType
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
        id = game.uniqueid.getUniqueId()
        characterType = message.characterType
        coordinates = message.spawnLocation

        name = "Bot " + str(id)
        # Enemy
        groupId = GroupId(id=id)
        enemy = self.world.create_entity()
        esperData = EsperData(self.world, enemy, name)
        tenemy = Enemy(name=name)
        ai = Ai(
            name=name,
            esperData=esperData,
            characterType=characterType)

        texture = CharacterTexture(
            characterAnimationType=CharacterAnimationType.standing,
            head=self.getRandomHead(),
            body=self.getRandomBody(),
            characterType=characterType,
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
        if characterType is CharacterType.stickfigure:
            offensiveAttack.switchWeapon(WeaponType.hitSquare)
        elif characterType is CharacterType.cow:
            offensiveAttack.switchWeapon(WeaponType.charge)

        self.world.add_component(enemy, ai)
        self.world.add_component(enemy, groupId)
        self.world.add_component(enemy, renderable)
        self.world.add_component(enemy, tenemy)
        self.world.add_component(enemy, Attackable(initialHealth=100))
        self.world.add_component(enemy, offensiveAttack)


    def getRandomHead(self):
        return random.choice(['^', 'o', 'O', 'v', 'V'])


    def getRandomBody(self):
        return random.choice(['X', 'o', 'O', 'v', 'V', 'M', 'm'])
