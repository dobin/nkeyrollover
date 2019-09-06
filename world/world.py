import logging
import random
import curses

from sprite.coordinates import Coordinates
from sprite.direction import Direction
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
from system.sceneprocessor import SceneProcessor
from system.renderableminimal import RenderableMinimal
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from system.offensiveattack import OffensiveAttack
from system.offensiveattackprocessor import OffensiveAttackProcessor
from system.movementprocessor import MovementProcessor
from entities.esperdata import EsperData
from system.inputprocessor import InputProcessor
from texture.character.characteranimationtype import CharacterAnimationType
from system.graphics.characteranimationprocessor import CharacterAnimationProcessor
from system.gamelogic.aiprocessor import AiProcessor
from system.renderableminimalprocessor import RenderableMinimalProcessor
from world.scenemanager import SceneManager
from world.statusbar import StatusBar
from utilities.entityfinder import EntityFinder

from messaging import messaging, Messaging, Message, MessageType

logger = logging.getLogger(__name__)


class World(object):
    """The game world in which all game object live"""

    def __init__(self, win, menuwin):
        self.esperWorld = esper.World()
        self.win = win
        self.statusBar = StatusBar(world=self, menuwin=menuwin)
        self.viewport :Viewport =Viewport(win=win, world=self)
        #self.worldSprite :Sprite = Sprite(viewport=self.viewport, parentSprite=None)
        self.particleEmiter :ParticleEmiter = ParticleEmiter(viewport=self.viewport)
        self.textureEmiter :TextureEmiter = TextureEmiter(
            viewport=self.viewport,
            esperWorld=self.esperWorld)
        self.map :Map = Map(viewport=self.viewport, world=self)
        self.sceneManager = SceneManager(
            viewport=self.viewport,
            esperWorld=self.esperWorld)

        self.pause :bool = False
        self.gameRunning :bool = True
        self.gameTime :float =0.0
        self.showStats = False
        self.showEnemyWanderDestination = False

        aiProcessor = AiProcessor()
        characterAnimationProcessor = CharacterAnimationProcessor(
            textureEmiter=self.textureEmiter
        )
        renderableProcessor = RenderableProcessor()
        advanceableProcessor = AdvanceableProcessor()
        playerProcessor = PlayerProcessor(viewport=self.viewport, particleEmiter=self.particleEmiter)
        enemyProcessor = EnemyProcessor(viewport=self.viewport)
        attackableProcessor = AttackableProcessor()
        offensiveAttackProcessor = OffensiveAttackProcessor()
        offensiveSkillProcessor = OffensiveSkillProcessor()
        movementProcessor = MovementProcessor()
        inputProcessor = InputProcessor()
        self.inputProcessor = inputProcessor # for Statusbar:APM
        renderableMinimalProcessor = RenderableMinimalProcessor(
            viewport=self.viewport,
            textureEmiter=self.textureEmiter)
        sceneProcessor = SceneProcessor(
            viewport=self.viewport,
            sceneManager=self.sceneManager,
        )

        # Lots of comments to check if the order of the processors really work,
        # as Messaging looses all messages on every iteration (use DirectMessaging 
        # instead)

        # KeyboardInput:getInput()
        # p generate  MessageType         PlayerKeypress

        # p handle:   MessageType         PlayerKeyPress (movement)
        # p generate: DirectMessageType   movePlayer
        self.esperWorld.add_processor(inputProcessor)

        # p handle:   DirectMessageType   movePlayer
        # e handle:   DirectMessageType   moveEnemy
        # p generate: MessageType         PlayerLocation
        # x generate: MessageType         EntityMoved
        self.esperWorld.add_processor(movementProcessor)

        # e handle:   MessageType         PlayerLocation
        # e generate: MessageType         EnemyAttack
        # e generate: DirectMessageType   moveEnemy
        # x generate: MessageType         EmitTextureMinimal
        self.esperWorld.add_processor(aiProcessor)

        # e handle:   DirectMessageType   moveEnemy
        # p handle:   MessageType         PlayerKeyPress (space/attack, weaponselect)
        # p generate: MessageType         PlayerAttack (via OffensiveAttackEntity)
        self.esperWorld.add_processor(offensiveAttackProcessor)

        # p handle:   MessageType         PlayerKeyPress (skill activate)
        # p generate: MessageType         PlayerAttack
        self.esperWorld.add_processor(offensiveSkillProcessor)

        # p handle:   MessageType         PlayerLocation
        self.esperWorld.add_processor(sceneProcessor)

        # x handle:   DirectMessageType   receiveDamage
        # x generate: MessageType         EntityStun
        # e generate: MessageType         EntityDying
        self.esperWorld.add_processor(attackableProcessor)

        # e handle:  MessageType          EntityDying
        # p handle:  MessageType          PlayerAttack
        # x handle:  MessageType          AttackWindup
        # x handle:  MessageType          EntityAttack
        # x handle:  MessageType          EntityMoved
        # x handle:  MessageType          EntityStun
        self.esperWorld.add_processor(characterAnimationProcessor)

        # Nothing
        self.esperWorld.add_processor(enemyProcessor)
        self.esperWorld.add_processor(playerProcessor)
        self.esperWorld.add_processor(advanceableProcessor)

        # x handle:  MessageType           EmitTextureMinimal
        self.esperWorld.add_processor(renderableMinimalProcessor)

        # p handle:   MessageType         PlayerAttack
        # e handle:   MessageType         EnemyAttack
        # x generate: DirectMessageType   receiveDamage
        self.esperWorld.add_processor(renderableProcessor)



    def togglePause(self):
        self.pause = not self.pause


    def toggleStats(self):
        self.showStats = not self.showStats


    def toggleShowEnemyWanderDestination(self):
        self.showEnemyWanderDestination = not self.showEnemyWanderDestination


    def draw(self, frame):
        # order here is relevant, as it is Z order 

        if self.sceneManager.currentScene.showMap():
            self.statusBar.drawStatusbar()
            self.map.draw()

        self.particleEmiter.draw()

        if self.showStats and frame % 10 == 0:
            self.drawStats()

        if frame % 100 == 0:
            self.printEntityStats()


        if self.pause:
            self.win.addstr(12, 40, "Paused", curses.color_pair(7))


    def printEntityStats(self): 
        renderableMinimal = 0
        for ent, rend in self.esperWorld.get_component(RenderableMinimal):
            renderableMinimal += 1

        renderable = 0
        for ent, rend in self.esperWorld.get_component(Renderable):
            renderable += 1

        logger.info("Stats: Renderable: {}  RenderableMinimal: {}".format(
            renderable, renderableMinimal
        ))


    def getGameTime(self):
        return self.gameTime


    def advance(self, deltaTime):
        if self.pause:
            return

        self.esperWorld.process(deltaTime)

        self.gameTime += deltaTime
        self.map.advance(deltaTime)
        self.particleEmiter.advance(deltaTime)

        messaging.reset()


    def drawStats(self):
        x = 4
        y = 4

        o = []

        o.append('Enemies:')
        o.append('  Alive     : ' 
            + str( EntityFinder.numEnemies(world=self.esperWorld)) )
        o.append('  Attacking : ' 
            + str( EntityFinder.numEnemiesInState(world=self.esperWorld, state='attack')) )
        o.append('  Chasing   : ' 
            + str( EntityFinder.numEnemiesInState(world=self.esperWorld, state='chase')) )
        o.append('  Wadndering: ' 
            + str( EntityFinder.numEnemiesInState(world=self.esperWorld, state='wander')) )

        playerEntity = EntityFinder.findPlayer(self.esperWorld)
        playerRenderable = self.esperWorld.component_for_entity(
            playerEntity, Renderable)

        o.append('Player:')
        o.append('  Location:' + str( playerRenderable.getLocation() ) )

        n = 0
        while n < len(o):
            self.win.addstr(y + n, x, o[n])
            n += 1


    def quitGame(self):
        self.gameRunning = False
