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
import esper
from system.advanceable import Advanceable, AdvanceableProcessor
from system.renderable import Renderable, RenderableProcessor
from system.gamelogic.attackable import Attackable
from system.gamelogic.attackableprocessor import AttackableProcessor
from system.gamelogic.tenemy import tEnemy, tEnemyProcessor
from system.gamelogic.tplayer import tPlayer, tPlayerProcessor
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from system.offensiveattack import OffensiveAttack
from system.offensiveattackprocessor import OffensiveAttackProcessor

from messaging import messaging, Messaging, Message, MessageType

logger = logging.getLogger(__name__)


class World(object): 
    """The game world in which all game object live"""

    def addPlayer(self): 
        # Player
        self.player = self.esperWorld.create_entity()
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
        renderable.name = "Player"
        self.esperWorld.add_component(self.player, renderable)
        self.esperWorld.add_component(self.player, tPlayer(renderable=renderable))
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
            z=3)
        renderable.name = "PlayerWeapon"
        texture.parentSprite = renderable
        self.esperWorld.add_component(characterAttackEntity, renderable)
        offensiveAttack = OffensiveAttack(
            isPlayer=True, 
            world=self,
            renderable=renderable)
        self.esperWorld.add_component(characterAttackEntity, offensiveAttack)
        self.characterAttackEntity = characterAttackEntity
        # /CharacterAttack

    def __init__(self, win):
        self.esperWorld = esper.World()
        self.win = win
        self.viewport :Viewport =Viewport(win=win, world=self)
        self.worldSprite :Sprite = Sprite(viewport=self.viewport, parentSprite=None)
        self.messaging = messaging

        self.addPlayer()

        self.director :Director = Director(self.viewport, self)
        self.director.init()
        self.particleEmiter :ParticleEmiter = ParticleEmiter(viewport=self.viewport)
        self.textureEmiter :TextureEmiter = TextureEmiter(viewport=self.viewport)
        self.map :Map = Map(viewport=self.viewport, world=self)
        
        self.pause :bool = False
        self.gameRunning :bool = True
        self.gameTime :float =0.0
        self.showStats = False
        self.showEnemyWanderDestination = False

        renderableProcessor = RenderableProcessor()
        advanceableProcessor = AdvanceableProcessor()
        tplayerProcessor = tPlayerProcessor()
        tenemyProcessor = tEnemyProcessor()
        attackableProcessor = AttackableProcessor()
        offensiveAttackProcessor = OffensiveAttackProcessor(
            playerAttackEntity=self.characterAttackEntity
        )
        
        self.esperWorld.add_processor(renderableProcessor)
        self.esperWorld.add_processor(advanceableProcessor)
        self.esperWorld.add_processor(tplayerProcessor)  
        self.esperWorld.add_processor(tenemyProcessor)  
        self.esperWorld.add_processor(attackableProcessor)          
        self.esperWorld.add_processor(offensiveAttackProcessor)          


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
