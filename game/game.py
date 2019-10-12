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
from system.gamelogic.gametimeprocessor import GametimeProcessor
from game.scenemanager import SceneManager
from game.statusbar import StatusBar
from game.enemyloader import EnemyLoader
from utilities.entityfinder import EntityFinder
from messaging import messaging
from directmessaging import directMessaging
from system.singletons.renderablecache import renderableCache
from system.gamelogic.damageprocessor import DamageProcessor
from texture.filetextureloader import fileTextureLoader
from game.offenseloader.fileoffenseloader import fileOffenseLoader

logger = logging.getLogger(__name__)


class Game(object):
    def __init__(self, win, menuwin):
        self.win = win

        self.world :esper.World = esper.World()
        self.statusBar :StatusBar = StatusBar(world=self, menuwin=menuwin)
        self.pause :bool = False
        self.gameRunning :bool = True
        self.showStats = False
        self.showLog = False

        fileTextureLoader.loadFromFiles()
        fileOffenseLoader.loadFromFiles()

        viewport :Viewport = Viewport(win=win, world=self)
        textureEmiter :TextureEmiter = TextureEmiter(
            viewport=viewport,
            world=self.world)
        mapManager :MapManager = MapManager(viewport=viewport)
        sceneManager :SceneManager = SceneManager(
            viewport=viewport,
            world=self.world,
            mapManager=mapManager)
        enemyLoader :EnemyLoader = EnemyLoader()
        renderableCache.init(viewport=viewport)


        particleProcessor = ParticleProcessor(viewport=viewport)
        gametimeProcessor = GametimeProcessor()
        aiProcessor = AiProcessor()
        characterAnimationProcessor = CharacterAnimationProcessor()
        playerProcessor = PlayerProcessor(
            viewport=viewport)
        enemyProcessor = EnemyProcessor(
            viewport=viewport, enemyLoader=enemyLoader)
        attackableProcessor = AttackableProcessor()
        offensiveAttackProcessor = OffensiveAttackProcessor()
        offensiveSkillProcessor = OffensiveSkillProcessor()
        movementProcessor = MovementProcessor(mapManager)
        inputProcessor = InputProcessor()
        renderableProcessor = RenderableProcessor(textureEmiter=textureEmiter)
        renderableMinimalProcessor = RenderableMinimalProcessor(
            viewport=viewport,
            textureEmiter=textureEmiter)
        sceneProcessor = SceneProcessor(
            viewport=viewport,
            sceneManager=sceneManager,
        )
        damageProcessor = DamageProcessor()

        self.viewport :Viewport = viewport  # for keybaordinput
        self.sceneProcessor :SceneProcessor = sceneProcessor  # for stats
        self.mapManager :MapManager = mapManager  # to advance it
        self.sceneManager :SceneManager = sceneManager  # to check for shopmap

        # Lots of comments to check if the order of the processors really work,
        # as Messaging looses all messages on every iteration (use DirectMessaging
        # instead)
        self.world.add_processor(gametimeProcessor)

        # KeyboardInput:getInput()
        # p generate: Message            PlayerKeypress

        # p handle:   Message            PlayerKeyPress (movement)
        # p generate: DirectMessage      movePlayer
        self.world.add_processor(inputProcessor)

        # p handle:   DirectMessage      movePlayer
        # e handle:   DirectMessage      moveEnemy
        # p generate: Message            PlayerLocation
        # x generate: Message            EntityMoved
        self.world.add_processor(movementProcessor)

        # p handle:   Message            PlayerLocation
        # e generate: DirectMessage      moveEnemy
        # x generate: Message            EmitTextureMinimal
        self.world.add_processor(aiProcessor)

        # e handle:   DirectMessage      moveEnemy
        # p handle:   Message            PlayerKeyPress (space/attack, weaponselect)
        # p generate: Message            PlayerAttack (via OffensiveAttack)
        # x generate: Message            AttackAt (via OffensiveAttack)
        # x generate: Message            EmitActionTexture (via OffensiveAttack)
        # x generate: Message            EmitTextureMinimal (via OffensiveAttack)
        self.world.add_processor(offensiveAttackProcessor)

        # p handle:   Message            PlayerKeyPress (skill activate)
        # x generate: Message            EmitParticleEffect (skill)
        # x generate: DirectMessage      activateSpeechBubble
        self.world.add_processor(offensiveSkillProcessor)

        # x handle:   DirectMessage      receiveDamage
        # x generate: Message            EntityStun
        # x generate: Message            EntityDying
        # x generate: Message            EmitTexture
        self.world.add_processor(attackableProcessor)

        # p handle:   Message            PlayerLocation
        # x handle:   Message            EntityDying
        # p handle:   Message            PlayerKeypress
        # e generate: Message            SpawnEnemy
        # p generate: Message            SpawnPlayer
        # x generate: DirectMessage      activateSpeechBubble
        self.world.add_processor(sceneProcessor)

        # e handle:   Message            SpawnEnemy
        # e generate: Message            EntityAttack
        # x generate: Message            EntityDead
        self.world.add_processor(enemyProcessor)

        # p handle:   Message            SpawnPlayer
        # p handle:   Message            PlayerAttack
        self.world.add_processor(playerProcessor)

        # x handle:   Message            EmitTextureMinimal
        # x handle:   Message            EmitTexture
        self.world.add_processor(renderableMinimalProcessor)

        # e handle:   Message            EntityDying
        # p handle:   Message            PlayerAttack
        # x handle:   Message            AttackWindup
        # x handle:   Message            EntityAttack
        # x handle:   Message            EntityMoved
        # x handle:   Message            EntityStun
        self.world.add_processor(characterAnimationProcessor)

        # x handle:   DirectMessage      activateSpeechBubble (emit)
        # x generate: Message            AttackAt
        # x generate: DirectMessage      activateSpeechBubble (because of damage)
        self.world.add_processor(renderableProcessor)

        # x handle:   Message            EmitParticleEffect
        # x generate: Message            AttackAt
        self.world.add_processor(particleProcessor)

        # x handle:   Message            AttackAt
        # x generate: DirectMessage      receiveDamage
        self.world.add_processor(damageProcessor)


    def draw1(self, frame :int):
        """Draws backmost layer (e.g. map)"""
        if self.sceneManager.currentScene.showMap():
            self.statusBar.drawStatusbar()
            self.mapManager.draw()


    def advance(self, deltaTime :float, frame :int):
        """Advance game, and draw game entities (e.g. player, effects)"""
        if self.pause:
            return

        messaging.setFrame(frame)
        directMessaging.setFrame(frame)

        self.world.process(deltaTime)  # this also draws
        self.mapManager.advance(deltaTime)

        messaging.reset()


    def draw2(self, frame :int):
        """Draws foremost layer (e.g. "pause" sign)"""
        if self.showStats:
            self.drawStats()

        # not drawing related, but who cares
        if frame % 1000 == 0:
            self.logEntityStats()

        if self.pause:
            self.win.addstr(12, 40, "Paused", curses.color_pair(7))


    def logEntityStats(self):
        renderableMinimal = 0
        for ent, rend in self.world.get_component(RenderableMinimal):
            renderableMinimal += 1

        renderable = 0
        for ent, rend in self.world.get_component(Renderable):
            renderable += 1

        logger.info("Stats: Renderable: {}  RenderableMinimal: {}".format(
            renderable, renderableMinimal
        ))


    def drawStats(self):
        x = 2
        y = 1

        o = []

        enemiesAlive = EntityFinder.numEnemies(
            world=self.world)
        enemiesAttacking = EntityFinder.numEnemiesInState(
            world=self.world, state='attack')
        enemiesChasing = EntityFinder.numEnemiesInState(
            world=self.world, state='chase')
        enemiesWandering = EntityFinder.numEnemiesInState(
            world=self.world, state='wander')

        o.append("Enemies:")
        o.append("  Alive     : {}".format(enemiesAlive))
        o.append("  Attacking : {}".format(enemiesAttacking))
        o.append("  Chasing   : {}".format(enemiesChasing))
        o.append("  Wandering: {}".format(enemiesWandering))

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


    def toggleLog(self):
        self.showLog = not self.showLog
