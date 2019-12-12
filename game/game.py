import logging
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
from system.gamelogic.aiprocessor import AiProcessor
from system.gamelogic.gametimeprocessor import GametimeProcessor
from system.gamelogic.damageprocessor import DamageProcessor
from system.gamelogic.passiveattackprocessor import PassiveAttackProcessor
from system.gamelogic.defenseprocessor import DefenseProcessor
from system.io.inputprocessor import InputProcessor
from system.graphics.characteranimationprocessor import CharacterAnimationProcessor
from system.graphics.renderableminimalprocessor import RenderableMinimalProcessor
from system.graphics.environmentprocessor import EnvironmentProcessor
from system.singletons.particleemiter import ParticleEmiter
from system.gamelogic.onhitprocessor import OnhitProcessor
from system.graphics.particleemiterprocessor import ParticleEmiterProcessor
from system.graphics.particlemirageemiterprocessor import ParticleMirageEmiterProcessor
from game.scenemanager import SceneManager
from game.statusbar import StatusBar
from utilities.entityfinder import EntityFinder
from messaging import messaging
from directmessaging import directMessaging
from system.singletons.renderablecache import renderableCache
from texture.filetextureloader import fileTextureLoader
from game.offenseloader.fileoffenseloader import fileOffenseLoader
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from utilities.colortype import ColorType
from config import Config

logger = logging.getLogger(__name__)


class Game(object):
    def __init__(self, win, menuwin):
        self.pause :bool = False
        self.gameRunning :bool = True
        self.showStats = False
        self.showLog = False

        self.win = win
        self.world :esper.World = esper.World()

        viewport :Viewport = Viewport(win=win, world=self)
        self.statusBar :StatusBar = StatusBar(world=self, viewport=viewport)

        fileTextureLoader.loadFromFiles()
        fileOffenseLoader.loadFromFiles()

        textureEmiter :TextureEmiter = TextureEmiter(
            viewport=viewport,
            world=self.world)
        mapManager :MapManager = MapManager(viewport=viewport)
        sceneManager :SceneManager = SceneManager(
            viewport=viewport,
            world=self.world,
            mapManager=mapManager)
        renderableCache.init(viewport=viewport)
        particleEmiter = ParticleEmiter(viewport=viewport)

        particleProcessor = ParticleProcessor(
            viewport=viewport, particleEmiter=particleEmiter)
        gametimeProcessor = GametimeProcessor()
        aiProcessor = AiProcessor()
        characterAnimationProcessor = CharacterAnimationProcessor()
        playerProcessor = PlayerProcessor(
            viewport=viewport)
        enemyProcessor = EnemyProcessor(
            viewport=viewport)
        attackableProcessor = AttackableProcessor()
        offensiveAttackProcessor = OffensiveAttackProcessor()
        offensiveSkillProcessor = OffensiveSkillProcessor()
        movementProcessor = MovementProcessor(mapManager)
        inputProcessor = InputProcessor()
        renderableProcessor = RenderableProcessor(
            textureEmiter=textureEmiter,
            particleEmiter=particleEmiter)
        renderableMinimalProcessor = RenderableMinimalProcessor(
            viewport=viewport,
            textureEmiter=textureEmiter)
        sceneProcessor = SceneProcessor(
            viewport=viewport,
            sceneManager=sceneManager,
        )
        particleEmiterProcessor = ParticleEmiterProcessor(
            particleEmiter=particleEmiter
        )
        damageProcessor = DamageProcessor()
        environmentProcessor = EnvironmentProcessor(
            viewport=viewport, mapManager=mapManager)
        passiveAttackProcessor = PassiveAttackProcessor()
        defenseProcessor = DefenseProcessor()
        onhitProcessor = OnhitProcessor()
        emitMirageParticleEffect = ParticleMirageEmiterProcessor(
            particleEmiter=particleEmiter
        )

        self.sceneProcessor :SceneProcessor = sceneProcessor  # show F1 stats
        self.viewport :Viewport = viewport  # for keyboardinput in nkeyrollover.py
        self.mapManager :MapManager = mapManager  # map is handled here in game
        self.sceneManager :SceneManager = sceneManager  # to check for showmap here in game

        self.bg = self.createBg(Config.columns, Config.rows)

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
        # p generate: Message            EmitMirageParticleEffect (appear)
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

        # x handle:   Message            EmitParticleEffect
        # x generate: Message            AttackAt (for skills)
        self.world.add_processor(particleEmiterProcessor)

        # x generate: Message            AttackAt (passive DoT)
        self.world.add_processor(passiveAttackProcessor)

        # x generate: Message            AttackAt (via particle, dmg on move)
        self.world.add_processor(particleProcessor)

        # x handle:   Message            AttackAt
        # x generate: Message            EmitMirageParticleEffect (impact)
        self.world.add_processor(onhitProcessor)
        
        # x handle:   Message            AttackAt
        # x generate: DirectMessage      receiveDamage
        self.world.add_processor(damageProcessor)

        # x change:   Message            receiveDamage
        # x generate: Message            EmitMirageParticleEffect (floating 'Blocked')
        self.world.add_processor(defenseProcessor)

        # x handle:   DirectMessage      receiveDamage
        # x generate: Message            EntityStun
        # x generate: Message            EntityEndStun
        # x generate: Message            EntityDying
        # x generate: Message            EmitTexture
        # x generate: Message            Gameover
        # x generate: Message            EmitMirageParticleEffect (floating Damage)
        self.world.add_processor(attackableProcessor)

        # x handle:   Message            EmitMirageParticleEffect
        self.world.add_processor(emitMirageParticleEffect)

        # p handle:   Message            PlayerLocation
        # x handle:   Message            EntityDying
        # p handle:   Message            PlayerKeypress
        # x handle:   Message            Gameover
        # e generate: Message            SpawnEnemy
        # p generate: Message            SpawnPlayer
        # x generate: DirectMessage      activateSpeechBubble
        # x generate: Message            ScreenMove
        # x generate: Message            GameStart
        self.world.add_processor(sceneProcessor)

        # x handle:   Message            ScreenMove
        # x handle:   Message            GameStart
        self.world.add_processor(environmentProcessor)

        # e handle:   Message            SpawnEnemy
        # e generate: Message            EntityAttack
        # x generate: Message            EntityDead
        self.world.add_processor(enemyProcessor)

        # p handle:   Message            SpawnPlayer
        # p handle:   Message            PlayerAttack
        self.world.add_processor(playerProcessor)

        # e handle:   Message            EntityDying
        # p handle:   Message            PlayerAttack
        # x handle:   Message            AttackWindup
        # x handle:   Message            EntityAttack
        # x handle:   Message            EntityMoved
        # x handle:   Message            EntityStun
        # x handle:   Message            EntityEndStun
        self.world.add_processor(characterAnimationProcessor)

        # x handle:   Message            EmitTextureMinimal
        # x handle:   Message            EmitTexture
        self.world.add_processor(renderableMinimalProcessor)

        # x handle:   DirectMessage      activateSpeechBubble (emit)
        # x generate: DirectMessage      activateSpeechBubble (because of damage)
        self.world.add_processor(renderableProcessor)


    def draw1(self, frame :int):
        """Draws backmost layer (e.g. map)"""
        # clear buffer
        self.viewport.win._buffer._double_buffer = self.copyBg()

        if self.sceneManager.currentScene.showMap():
            self.mapManager.draw()


    def copyBg(self):
        box = [line[:] for line in self.bg]
        return box


    def createBg(self, width, height, uni=False):
        box = []
        width = self.viewport.win._buffer._width
        height = self.viewport.win._buffer._height

        fg, attr = ColorPalette.getColorByColor(Color.black)
        bg, _ = ColorPalette.getColorByColor(Color.black)
        w = 1

        tl = (ord(u"┌"), fg, attr, bg, w)
        tr = (ord(u"┐"), fg, attr, bg, w)
        bl = (ord(u"└"), fg, attr, bg, w)
        br = (ord(u"┘"), fg, attr, bg, w)
        h = (ord(u"─"), fg, attr, bg, w)
        v = (ord(u"│"), fg, attr, bg, w)
        s = (ord(u" "), fg, attr, bg, w)

        meWidth = Config.columns
        meHeight = Config.rows

        # top line
        line = []
        line.append(tl)
        n = 0
        while n < meWidth - 2:
            line.append(h)
            n += 1
        line.append(tr)
        while n < width:
            line.append(s)
            n += 1
        box.append(line)

        # middle
        line = []
        line.append(v)
        n = 0
        while n < meWidth - 2:
            line.append(s)
            n += 1
        line.append(v)

        # rest
        while n < width:
            line.append(s)
            n += 1
        for _ in range(meHeight - 2):
            box.append(line)

        # bottom line
        line = []
        line.append(bl)
        n = 0
        while n < meWidth - 2:
            line.append(h)
            n += 1
        line.append(br)
        while n < width:
            line.append(s)
            n += 1
        box.append(line)

        # rest
        y = meHeight
        while y < height:
            line = []
            n = 0
            while n < width:
                line.append(s)
                n += 1
            y += 1
            box.append(line)

        return box


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
        if self.sceneManager.currentScene.showMap():
            self.statusBar.drawStatusbar()

        if self.showStats:
            self.drawStats()

        # not drawing related, but who cares
        if frame % 1000 == 0:
            self.logEntityStats()

        if self.pause:
            color, attr = ColorPalette.getColorByColor(Color.white)
            self.viewport.addstr(
                12,
                40,
                "Paused",
                color,
                attr)


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
        color, attr = ColorPalette.getColorByColorType(ColorType.menu)

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
            self.viewport.addstr(y + n, x, o[n], color=color, attr=attr)
            n += 1


    def quitGame(self):
        self.gameRunning = False


    def togglePause(self):
        self.pause = not self.pause


    def toggleStats(self):
        self.showStats = not self.showStats


    def toggleLog(self):
        self.showLog = not self.showLog
