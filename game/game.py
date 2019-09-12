import logging
import curses
import esper

from system.graphics.particleprocessor import ParticleProcessor
from .mapmanager import MapManager
from .viewport import Viewport
from .textureemiter import TextureEmiter
from system.graphics.renderable import Renderable
from system.graphics.renderableprocessor import RenderableProcessor
from system.gamelogic.attackableprocessor import AttackableProcessor
from system.gamelogic.enemyprocessor import EnemyProcessor
from system.gamelogic.playerprocessor import PlayerProcessor
from system.gamelogic.offensiveskillprocessor import OffensiveSkillProcessor
from system.graphics.sceneprocessor import SceneProcessor
from system.graphics.renderableminimal import RenderableMinimal
from system.gamelogic.offensiveattackprocessor import OffensiveAttackProcessor
from system.gamelogic.movementprocessor import MovementProcessor
from system.io.inputprocessor import InputProcessor
from system.graphics.characteranimationprocessor import CharacterAnimationProcessor
from system.gamelogic.aiprocessor import AiProcessor
from system.graphics.renderableminimalprocessor import RenderableMinimalProcessor
from game.scenemanager import SceneManager
from game.statusbar import StatusBar
from utilities.entityfinder import EntityFinder
from messaging import messaging
from directmessaging import directMessaging
from game.particleemiter import ParticleEmiter

logger = logging.getLogger(__name__)


class Game(object):
    """The game world in which all game object live"""

    def __init__(self, win, menuwin):
        self.win = win

        self.world = esper.World()
        self.statusBar = StatusBar(world=self, menuwin=menuwin)
        self.viewport :Viewport = Viewport(win=win, world=self)
        self.textureEmiter :TextureEmiter = TextureEmiter(
            viewport=self.viewport,
            world=self.world)
        self.mapManager :MapManager = MapManager(viewport=self.viewport)
        self.sceneManager = SceneManager(
            viewport=self.viewport,
            world=self.world,
            mapManager=self.mapManager)
        self.particleEmiter = ParticleEmiter()

        self.pause :bool = False
        self.gameRunning :bool = True
        self.gameTime :float = 0.0
        self.showStats = False
        self.showEnemyWanderDestination = False

        particleProcessor = ParticleProcessor(viewport=self.viewport)

        aiProcessor = AiProcessor()
        characterAnimationProcessor = CharacterAnimationProcessor()
        renderableProcessor = RenderableProcessor()
        playerProcessor = PlayerProcessor(
            viewport=self.viewport)
        enemyProcessor = EnemyProcessor(viewport=self.viewport)
        attackableProcessor = AttackableProcessor()
        offensiveAttackProcessor = OffensiveAttackProcessor()
        offensiveSkillProcessor = OffensiveSkillProcessor()
        movementProcessor = MovementProcessor()
        inputProcessor = InputProcessor()
        self.inputProcessor = inputProcessor  # for Statusbar:APM
        renderableMinimalProcessor = RenderableMinimalProcessor(
            viewport=self.viewport,
            textureEmiter=self.textureEmiter)
        sceneProcessor = SceneProcessor(
            viewport=self.viewport,
            sceneManager=self.sceneManager,
        )
        self.sceneProcessor = sceneProcessor  # for stats

        # Lots of comments to check if the order of the processors really work,
        # as Messaging looses all messages on every iteration (use DirectMessaging 
        # instead)

        # KeyboardInput:getInput()
        # p generate  MessageType         PlayerKeypress

        # p handle:   MessageType         PlayerKeyPress (movement)
        # p generate: DirectMessageType   movePlayer
        self.world.add_processor(inputProcessor)

        # p handle:   DirectMessageType   movePlayer
        # e handle:   DirectMessageType   moveEnemy
        # p generate: MessageType         PlayerLocation
        # x generate: MessageType         EntityMoved
        self.world.add_processor(movementProcessor)

        # e handle:   MessageType         PlayerLocation
        # e generate: MessageType         EnemyAttack
        # e generate: DirectMessageType   moveEnemy
        # x generate: MessageType         EmitTextureMinimal
        # e generate: MessageType         EntityDead
        self.world.add_processor(aiProcessor)

        # e handle:   DirectMessageType   moveEnemy
        # p handle:   MessageType         PlayerKeyPress (space/attack, weaponselect)
        # p generate: MessageType         PlayerAttack. (via OffensiveAttack)
        self.world.add_processor(offensiveAttackProcessor)

        # p handle:   MessageType         PlayerKeyPress (skill activate)
        # p generate: MessageType         PlayerAttack!
        # p generate: MessageType         EmitParticleEffect (skill)
        self.world.add_processor(offensiveSkillProcessor)

        # x handle:   MessageType         EmitTextureMinimal
        # p generate: MessageType         PlayerAttack. (via texture emiter)
        self.world.add_processor(renderableMinimalProcessor)

        # p handle:   MessageType         PlayerLocation
        # e handle:   MessageType         EntityDead
        self.world.add_processor(sceneProcessor)

        # x handle:   DirectMessageType   receiveDamage
        # x generate: MessageType         EntityStun
        # e generate: MessageType         EntityDying
        self.world.add_processor(attackableProcessor)

        # e handle:  MessageType          EntityDying
        # p handle:  MessageType          PlayerAttack.
        # x handle:  MessageType          AttackWindup
        # x handle:  MessageType          EntityAttack
        # x handle:  MessageType          EntityMoved
        # x handle:  MessageType          EntityStun
        self.world.add_processor(characterAnimationProcessor)

        # Nothing
        self.world.add_processor(enemyProcessor)
        self.world.add_processor(playerProcessor)


        # p handle:   MessageType         PlayerAttack. (convert to damage)
        # e handle:   MessageType         EnemyAttack
        # x generate: DirectMessageType   receiveDamage
        self.world.add_processor(renderableProcessor)

        # x handle:   MessageType         EmitParticleEffect
        # x generate: DirectMessageType   receiveDamage
        self.world.add_processor(particleProcessor)


    def draw1(self, frame):
        """Draws backmost layer (e.g. map)"""
        if self.sceneManager.currentScene.showMap():
            self.statusBar.drawStatusbar()
            self.mapManager.draw()


    def advance(self, deltaTime, frame):
        """Advance game, and draw game entities (e.g. player, effects)"""
        if self.pause:
            return

        messaging.setFrame(frame)
        directMessaging.setFrame(frame)
        self.gameTime += deltaTime

        self.world.process(deltaTime)  # this also draws
        self.mapManager.advance(deltaTime)

        messaging.reset()


    def draw2(self, frame):
        """Draws foremost layer (e.g. "pause" sign)"""
        if self.showStats:
            self.drawStats()

        # not drawing related, but who cares
        if frame % 100 == 0:
            self.printEntityStats()

        if self.pause:
            self.win.addstr(12, 40, "Paused", curses.color_pair(7))


    def printEntityStats(self): 
        renderableMinimal = 0
        for ent, rend in self.world.get_component(RenderableMinimal):
            renderableMinimal += 1

        renderable = 0
        for ent, rend in self.world.get_component(Renderable):
            renderable += 1

        logger.info("Stats: Renderable: {}  RenderableMinimal: {}".format(
            renderable, renderableMinimal
        ))


    def getGameTime(self):
        return self.gameTime


    def drawStats(self):
        x = 2
        y = 1

        o = []

        o.append('Enemies:')
        o.append('  Alive     : '
            + str(EntityFinder.numEnemies(world=self.world)))
        o.append('  Attacking : '
            + str(EntityFinder.numEnemiesInState(world=self.world, state='attack')))
        o.append('  Chasing   : '
            + str(EntityFinder.numEnemiesInState(world=self.world, state='chase')))
        o.append('  Wandering: '
            + str(EntityFinder.numEnemiesInState(world=self.world, state='wander')))

        playerEntity = EntityFinder.findPlayer(self.world)
        playerRenderable = self.world.component_for_entity(
            playerEntity, Renderable)

        o.append('Player:')
        o.append('  Location:' + str(playerRenderable.getLocation()))

        o.append('Scene:')
        o.append('  Name:' + self.sceneManager.currentScene.name)
        o.append('  Scne State:' + str(self.sceneProcessor.state))
        o.append('  Enemies Alive:' + str(self.sceneProcessor.numEnemiesAlive()))
        o.append('  Enemies Visible:' + str(self.sceneProcessor.numEnemiesVisible()))

        n = 0
        while n < len(o):
            self.win.addstr(y + n, x, o[n])
            n += 1


    def quitGame(self):
        self.gameRunning = False


    def togglePause(self):
        self.pause = not self.pause


    def toggleStats(self):
        self.showStats = not self.showStats


    def toggleShowEnemyWanderDestination(self):
        self.showEnemyWanderDestination = not self.showEnemyWanderDestination
