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
from common.direction import Direction
from system.graphics.physics import Physics
from game.playerseed import PlayerSeed
from system.gamelogic.defense import Defense

logger = logging.getLogger(__name__)


class PlayerProcessor(esper.Processor):
    def __init__(self, viewport):
        super().__init__()

        self.viewport = viewport
        self.playerSeed = PlayerSeed()


    def process(self, deltaTime):
        self.advance(deltaTime)
        self.checkSpawn()
        self.checkAttack()


    def checkAttack(self):
        for message in messaging.getByType(MessageType.PlayerAttack):
            # most likely just one such message
            playerEntity = EntityFinder.findPlayer(self.world)
            player = self.world.component_for_entity(
                playerEntity, system.gamelogic.player.Player)

            player.setAttacking(attackTime=message.data['attackAnimationLength'])


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
            initialHealth=self.playerSeed.initialHealth,
            stunCount=self.playerSeed.stunCount,
            stunTimeFrame=self.playerSeed.stunTimeFrame,
            stunTime=self.playerSeed.stunTime,
            knockdownChance=self.playerSeed.knockdownChance,
            knockbackChance=self.playerSeed.knockbackChance)
        texture = CharacterTexture(
            characterTextureType=CharacterTextureType.player,
            characterAnimationType=CharacterAnimationType.standing,
            name='Player')
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=spawnCoordinates,
            direction=Direction.right,
            name='Player',
            canMoveOutsideMap=False)
        esperData = EsperData(self.world, playerEntity, 'player')
        offensiveSkill = OffensiveSkill(
            esperData=esperData,
            viewport=self.viewport)
        offensiveAttack = OffensiveAttack(
            parentChar=player,
            parentRenderable=renderable)
        physics = Physics()
        defense = Defense()

        self.world.add_component(playerEntity, physics)
        self.world.add_component(playerEntity, groupId)
        self.world.add_component(playerEntity, offensiveSkill)
        self.world.add_component(playerEntity, renderable)
        self.world.add_component(playerEntity, player)
        self.world.add_component(playerEntity, attackable)
        self.world.add_component(playerEntity, offensiveAttack)
        self.world.add_component(playerEntity, defense)
