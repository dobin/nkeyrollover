import esper
import logging

import system.gamelogic.player
from messaging import messaging, MessageType
from sprite.coordinates import Coordinates
from config import Config
from texture.character.charactertype import CharacterType
from texture.character.charactertexture import CharacterTexture
from entities.esperdata import EsperData
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
    def __init__(self, viewport, particleEmiter):
        super().__init__()

        self.viewport = viewport
        self.particleEmiter = particleEmiter


    def process(self, deltaTime):
        self.advance(deltaTime)
        self.checkSpawn()


    def checkSpawn(self):
        for message in messaging.getByType(MessageType.SpawnPlayer):
            self.spawnPlayer()


    def advance(self, deltaTime):
        playerEntity = EntityFinder.findPlayer(self.world)
        if playerEntity is None: 
            return
        player = self.world.component_for_entity(
                playerEntity, Player)

        player.advance(deltaTime)


    def spawnPlayer(self):
        # Player
        myid = 0
        self.playerEntity = self.world.create_entity()
        esperData = EsperData(self.world, self.playerEntity, 'player')
        texture = CharacterTexture(
            characterType=CharacterType.player,
            characterAnimationType=CharacterAnimationType.standing)
        texture.name = "Player"
        coordinates = Coordinates(
            Config.playerSpawnPoint['x'],
            Config.playerSpawnPoint['y']
        )
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates)
        characterSkill = OffensiveSkill(
            esperData=esperData,
            particleEmiter=self.particleEmiter,
            viewport=self.viewport)
        self.characterSkillEntity = characterSkill
        renderable.name = "Player"
        groupId = GroupId(id=myid)
        player = system.gamelogic.player.Player()
        self.world.add_component(self.playerEntity, groupId)
        self.world.add_component(self.playerEntity, characterSkill)
        self.world.add_component(self.playerEntity, renderable)
        self.world.add_component(self.playerEntity, player)
        self.world.add_component(self.playerEntity, Attackable(initialHealth=100))
        self.playerRendable = renderable

        offensiveAttack = OffensiveAttack(
            parentChar=player,
            parentRenderable=renderable)
        self.world.add_component(self.playerEntity, offensiveAttack)
        # /Player
