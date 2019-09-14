import esper
import logging

import system.gamelogic.player
from messaging import messaging, MessageType
from texture.character.charactertexturetype import CharacterTextureType
from texture.character.charactertexture import CharacterTexture
from system.gamelogic.esperdata import EsperData
from texture.character.characteranimationtype import CharacterAnimationType
from system.graphics.renderable import Renderable
from system.gamelogic.offensiveskill import OffensiveSkill
from system.groupid import GroupId
from system.gamelogic.attackable import Attackable
from system.gamelogic.offensiveattack import OffensiveAttack
from utilities.entityfinder import EntityFinder
from system.gamelogic.player import Player

logger = logging.getLogger(__name__)


class PlayerProcessor(esper.Processor):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport


    def process(self, deltaTime):
        self.advance(deltaTime)
        self.checkSpawn()


    def checkSpawn(self):
        for message in messaging.getByType(MessageType.SpawnPlayer):
            self.spawnPlayer(message.data['coordinates'])


    def advance(self, deltaTime):
        playerEntity = EntityFinder.findPlayer(self.world)
        if playerEntity is None:
            return
        player = self.world.component_for_entity(
            playerEntity, Player)

        player.advance(deltaTime)


    def spawnPlayer(self, spawnCoordinates):
        myid = 0  # 0 should be player
        playerEntity = self.world.create_entity()
        groupId = GroupId(id=myid)
        player = system.gamelogic.player.Player()
        attackable = Attackable(
            initialHealth=1000,
            stunTime=0.75)

        texture = CharacterTexture(
            characterTextureType=CharacterTextureType.player,
            characterAnimationType=CharacterAnimationType.standing,
            name='Player')
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=spawnCoordinates,
            name='Player')

        esperData = EsperData(self.world, playerEntity, 'player')
        characterSkill = OffensiveSkill(
            esperData=esperData,
            viewport=self.viewport)

        offensiveAttack = OffensiveAttack(
            parentChar=player,
            parentRenderable=renderable)

        self.world.add_component(playerEntity, groupId)
        self.world.add_component(playerEntity, characterSkill)
        self.world.add_component(playerEntity, renderable)
        self.world.add_component(playerEntity, player)
        self.world.add_component(playerEntity, attackable)
        self.world.add_component(playerEntity, offensiveAttack)
