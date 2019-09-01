import logging
import random
import curses 

from sprite.coordinates import Coordinates
from sprite.direction import Direction
from world.director import Director
from config import Config
from entities.entity import Entity
from entities.entitytype import EntityType
from world.particleemiter import ParticleEmiter
from sprite.sprite import Sprite
from .map import Map
from .viewport import Viewport
from .textureemiter import TextureEmiter
from texture.character.charactertype import CharacterType
from texture.character.charactertexture import CharacterTexture
from texture.animationtexture import AnimationTexture

import esper
from system.advanceable import Advanceable, AdvanceableProcessor
from system.renderable import Renderable
from system.renderableprocessor import RenderableProcessor
from system.gamelogic.attackable import Attackable
from system.gamelogic.attackableprocessor import AttackableProcessor
from system.gamelogic.enemy import Enemy
from system.gamelogic.enemyprocessor import EnemyProcessor
from system.gamelogic.player import Player
from system.gamelogic.playerprocessor import PlayerProcessor
from system.offensiveskill import OffensiveSkill
from system.offensiveskillprocessor import OffensiveSkillProcessor
from system.graphics.speechbubble import SpeechBubble
from system.groupid import GroupId

from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from system.offensiveattack import OffensiveAttack
from system.offensiveattackprocessor import OffensiveAttackProcessor
from entities.esperdata import EsperData

from messaging import messaging, Messaging, Message, MessageType

logger = logging.getLogger(__name__)


class World(object): 
    """The game world in which all game object live"""

    def __init__(self, win):
        self.esperWorld = esper.World()
        self.win = win
        self.viewport :Viewport =Viewport(win=win, world=self)
        self.worldSprite :Sprite = Sprite(viewport=self.viewport, parentSprite=None)
        self.particleEmiter :ParticleEmiter = ParticleEmiter(viewport=self.viewport)
        self.textureEmiter :TextureEmiter = TextureEmiter(viewport=self.viewport)
        self.map :Map = Map(viewport=self.viewport, world=self)

        self.addPlayer()
        self.director :Director = Director(self.viewport, self)
        self.director.init()

        self.pause :bool = False
        self.gameRunning :bool = True
        self.gameTime :float =0.0
        self.showStats = False
        self.showEnemyWanderDestination = False

        renderableProcessor = RenderableProcessor()
        advanceableProcessor = AdvanceableProcessor()
        playerProcessor = PlayerProcessor()
        enemyProcessor = EnemyProcessor()
        attackableProcessor = AttackableProcessor()
        offensiveAttackProcessor = OffensiveAttackProcessor(
            playerAttackEntity=self.characterAttackEntity
        )
        offensiveSkillProcessor = OffensiveSkillProcessor(
            player=self.player,
        )

        self.esperWorld.add_processor(advanceableProcessor)
        self.esperWorld.add_processor(playerProcessor)  
        self.esperWorld.add_processor(enemyProcessor)  
        self.esperWorld.add_processor(attackableProcessor)          
        self.esperWorld.add_processor(offensiveAttackProcessor)
        self.esperWorld.add_processor(offensiveSkillProcessor)         
        self.esperWorld.add_processor(renderableProcessor)


    def addPlayer(self): 
        # Player
        myid = 31337
        self.player = self.esperWorld.create_entity()
        esperData = EsperData(self.esperWorld, self.player, 'player')
        texture = CharacterTexture(parentSprite=None, characterType=CharacterType.player)
        coordinates = Coordinates(
            Config.playerSpawnPoint['x'],
            Config.playerSpawnPoint['y']
        )
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates)
        texture.parentSprite = renderable
        characterSkill = OffensiveSkill(
            esperData=esperData, 
            particleEmiter=self.particleEmiter,
            viewport=self.viewport)
        self.characterSkillEntity = characterSkill
        renderable.name = "Player"
        groupId = GroupId(id=myid)
        self.esperWorld.add_component(self.player, groupId)
        self.esperWorld.add_component(self.player, characterSkill)
        self.esperWorld.add_component(self.player, renderable)
        self.esperWorld.add_component(self.player, Player(esperData=esperData))
        self.esperWorld.add_component(self.player, Attackable(initialHealth=100))
        self.playerRendable = renderable
        # /Player

        # CharacterAttack
        characterAttackEntity = self.esperWorld.create_entity()
        texture :PhenomenaTexture = PhenomenaTexture(phenomenaType=PhenomenaType.hit, parentSprite=self)
        coordinates = Coordinates( # for hit
            -1,
            1
        )
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=self.playerRendable,
            coordinates=coordinates,
            z=3,
            active=False,
            useParentDirection=True)
        renderable.name = "PlayerWeapon"
        texture.parentSprite = renderable
        self.esperWorld.add_component(characterAttackEntity, renderable)
        offensiveAttack = OffensiveAttack(
            isPlayer=True, 
            world=self,
            renderable=renderable)
        groupId = GroupId(id=myid)
        self.esperWorld.add_component(characterAttackEntity, groupId)
        self.esperWorld.add_component(characterAttackEntity, offensiveAttack)
        self.characterAttackEntity = characterAttackEntity
        # /CharacterAttack

        # speech
        speechEntity = self.esperWorld.create_entity()
        texture = AnimationTexture(parentSprite=None)
        coordinates = Coordinates(1, -4)
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=self.playerRendable,
            coordinates=coordinates,
            z=3,
            active=False)
        texture.parentSprite = renderable
        speechBubble = SpeechBubble(renderable=renderable)
        groupId = GroupId(id=myid)
        self.esperWorld.add_component(
            speechEntity, 
            groupId)
        self.esperWorld.add_component(
            speechEntity, 
            renderable)
        self.esperWorld.add_component(
            speechEntity, 
            speechBubble)
        # /speech


    def togglePause(self): 
        self.pause = not self.pause


    def toggleStats(self): 
        self.showStats = not self.showStats


    def toggleShowEnemyWanderDestination(self): 
        self.showEnemyWanderDestination = not self.showEnemyWanderDestination


    def draw(self):
        # order here is Z axis
        self.map.draw()
        self.textureEmiter.draw()
        self.particleEmiter.draw() # should be on top

        if self.showStats:
            self.drawStats()

        if self.pause: 
            self.win.addstr(12, 40, "Paused", curses.color_pair(7))


    def getGameTime(self): 
        return self.gameTime


    def advance(self, deltaTime):
        if self.pause:
            return

        self.esperWorld.process(deltaTime)

        self.gameTime += deltaTime
        self.map.advance(deltaTime)
        self.director.advanceEnemies(deltaTime)
        self.particleEmiter.advance(deltaTime)
        self.textureEmiter.advance(deltaTime)
        self.director.worldUpdate()
        self.viewport.advance(deltaTime)

        messaging.reset()


    def drawStats(self): 
        x = 4
        y = 4

        o = []

        o.append('Enemies:')
        o.append('  Alive     : ' + str( self.director.numEnemiesAlive() ))
        o.append('  Attacking : ' + str( self.director.numEnemiesAttacking() ))
        o.append('  Chasing   : ' + str( self.director.numEnemiesChasing() ))
        o.append('  Wadndering: ' + str( self.director.numEnemiesWandering() ))

        n = 0
        while n < len(o):
            self.win.addstr(y + n, x, o[n])
            n += 1


    def quitGame(self): 
        self.gameRunning = False
