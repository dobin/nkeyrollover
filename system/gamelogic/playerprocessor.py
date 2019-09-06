import esper
import logging

import system.gamelogic.player
from messaging import messaging, MessageType


from sprite.coordinates import Coordinates
from sprite.direction import Direction
from config import Config
from entities.entity import Entity
from entities.entitytype import EntityType
from world.particleemiter import ParticleEmiter
from sprite.sprite import Sprite
from texture.character.charactertype import CharacterType
from texture.character.charactertexture import CharacterTexture
from texture.animationtexture import AnimationTexture
from entities.esperdata import EsperData
from texture.character.characteranimationtype import CharacterAnimationType
from system.graphics.characteranimationprocessor import CharacterAnimationProcessor
from system.renderable import Renderable
from system.graphics.speechbubble import SpeechBubble
from system.offensiveskill import OffensiveSkill
from system.groupid import GroupId
from system.gamelogic.attackable import Attackable
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from system.offensiveattack import OffensiveAttack
import world.uniqueid
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
        self.player = self.world.create_entity()
        esperData = EsperData(self.world, self.player, 'player')
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
        self.world.add_component(self.player, groupId)
        self.world.add_component(self.player, characterSkill)
        self.world.add_component(self.player, renderable)
        self.world.add_component(self.player, system.gamelogic.player.Player())
        self.world.add_component(self.player, Attackable(initialHealth=100))
        self.playerRendable = renderable
        # /Player

        # CharacterAttack
        characterAttackEntity = self.world.create_entity()
        texture :PhenomenaTexture = PhenomenaTexture(
            phenomenaType=PhenomenaType.hit)
        coordinates = Coordinates( # for hit
            0,
            0
        )
        texture.name = "Playerweapon"
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=self.playerRendable,
            coordinates=coordinates,
            z=3,
            active=False,
            useParentDirection=True)
        renderable.setLocation(
           Coordinates(-1 * (renderable.texture.width - 2), -1)
        )            
        renderable.name = "PlayerWeapon"
        self.world.add_component(characterAttackEntity, renderable)
        offensiveAttack = OffensiveAttack(
            isPlayer=True,
            world=self,
            renderable=renderable)
        groupId = GroupId(id=myid)
        self.world.add_component(characterAttackEntity, groupId)
        self.world.add_component(characterAttackEntity, offensiveAttack)
        self.characterAttackEntity = characterAttackEntity
        # /CharacterAttack

        # speech
        speechEntity = self.world.create_entity()
        texture = AnimationTexture()
        coordinates = Coordinates(1, -4)
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=self.playerRendable,
            coordinates=coordinates,
            z=3,
            active=False)
        speechBubble = SpeechBubble(renderable=renderable)
        groupId = GroupId(id=myid)
        self.world.add_component(
            speechEntity,
            groupId)
        self.world.add_component(
            speechEntity,
            renderable)
        self.world.add_component(
            speechEntity,
            speechBubble)
        # /speech
