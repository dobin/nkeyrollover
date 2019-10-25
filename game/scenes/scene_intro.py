import logging
from enum import Enum

from utilities.timer import Timer
from game.scenes.scenebase import SceneBase
from common.coordinates import Coordinates
from common.direction import Direction
from system.graphics.renderable import Renderable
from config import Config
from texture.phenomena.phenomenatype import PhenomenaType
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexture import CharacterTexture
from texture.character.charactertexturetype import CharacterTextureType
from game.textureemiter import TextureEmiter
from system.singletons.renderablecache import renderableCache
from utilities.color import Color
from utilities.colorpalette import ColorPalette

logger = logging.getLogger(__name__)


class IntroSceneState(Enum):
    wait1 = 1       # wait 1s
    flydown = 2     # fly heli down
    drop = 3        # drop asciiman
    flyup = 4       # fly up
    spawnenemy = 5
    speakenemy = 6
    leaveenemy = 7
    done = 10        # start the game



class SceneIntro(SceneBase):
    def __init__(self, viewport, world):
        super().__init__(world=world, viewport=viewport)

        self.textureEmiter = TextureEmiter(viewport=viewport, world=world)
        renderableCache.init(viewport=viewport)

        textureCopter = PhenomenaTexture(
            phenomenaType=PhenomenaType.roflcopter,
            name="Scene1 chopper")
        self.copterSpawn = Coordinates(13, -1 * textureCopter.height)
        renderableCopter = Renderable(
            texture=textureCopter,
            viewport=self.viewport,
            coordinates=self.copterSpawn,
            active=True,
        )

        texturePlayer = CharacterTexture(
            characterAnimationType=CharacterAnimationType.standing,
            characterTextureType=CharacterTextureType.player,
            name='Scene1 Player')
        coordinates = Coordinates(24, 13)
        renderablePlayer = Renderable(
            texture=texturePlayer,
            viewport=self.viewport,
            coordinates=coordinates,
            active=True,
        )

        textureEnemy = CharacterTexture(
            characterAnimationType=CharacterAnimationType.standing,
            characterTextureType=CharacterTextureType.player,
            name='Scene1 Enemy')
        coordinates = Coordinates(Config.columns, 13)
        renderableEnemy = Renderable(
            texture=textureEnemy,
            viewport=self.viewport,
            coordinates=coordinates,
            active=True,
        )

        self.renderableCopter = renderableCopter
        self.renderablePlayer = renderablePlayer
        self.renderableEnemy = renderableEnemy

        self.myTimer = Timer(0.5)
        self.state = IntroSceneState.wait1
        self.name = "Scene1 - Intro Animation"
        self.anyKeyFinishesScene = True

        self.init()


    def advance(self, dt):
        self.myTimer.advance(dt)
        self.handleState()


    def enter(self):
        self.addRenderable(self.renderableCopter)


    def sceneIsFinished(self) -> bool:
        if self.state is IntroSceneState.done:
            return True
        else:
            return False


    def handleState(self):
        # interactive, aka a hack, but it works
        if (self.state is IntroSceneState.wait1
                or self.state is IntroSceneState.flydown
                or self.state is IntroSceneState.drop
                or self.state is IntroSceneState.flyup):

            c1, a1 = ColorPalette.getColorByColor(Color.blue)
            c2, a2 = ColorPalette.getColorByColor(Color.brightblue)
            self.viewport.addstr(5, 40,  "N Key Rollover", c1, a1)
            self.viewport.addstr(6, 40,  "Escape from Hong Kong", c2, a2)

            c3, a3 = ColorPalette.getColorByColor(Color.cyan)
            self.viewport.addstr(8, 40,  "Moving: arrow keys, shift to strafe", c3, a3)
            self.viewport.addstr(9, 40,  "Select attack: 1 2 3 4", c3, a3)
            self.viewport.addstr(10, 40, "Attack       : space", c3, a3)
            self.viewport.addstr(11, 40, "Skills       : q w e r", c3, a3)
            self.viewport.addstr(12, 40, "Heal, Port   : f g", c3, a3)

        # state
        if self.state is IntroSceneState.wait1:
            # for next scene: Flydown
            if self.myTimer.timeIsUp():
                self.state = IntroSceneState.flydown
                self.myTimer.setTimer(0.1)
                self.renderableCopter.setActive(True)
                logger.debug("Scene: Go to State: Flydown")

        elif self.state is IntroSceneState.flydown:
            if self.myTimer.timeIsUp():
                self.myTimer.reset()
                self.renderableCopter.coordinates.y += 1

            # for next scene: Drop
            if self.renderableCopter.coordinates.y == 8:
                self.myTimer.setTimer(0.1)
                logger.debug("Scene: Go to State: Drop")
                self.addRenderable(self.renderablePlayer)
                self.state = IntroSceneState.drop

        elif self.state is IntroSceneState.drop:
            # for next scene: Flyup
            if self.myTimer.timeIsUp():
                self.myTimer.reset()
                self.renderableCopter.coordinates.y -= 1

            if self.renderableCopter.coordinates.y == self.copterSpawn.y:
                self.myTimer.setTimer(0.1)
                self.addRenderable(self.renderableEnemy)
                self.renderableEnemy.texture.changeAnimation(
                    CharacterAnimationType.walking, direction=Direction.left)
                self.state = IntroSceneState.spawnenemy
                self.isShowMap = True
                logger.info("Scene: Go to State: SpawnEnemy")

        elif self.state is IntroSceneState.spawnenemy:
            if self.myTimer.timeIsUp():
                self.myTimer.reset()
                self.renderableEnemy.coordinates.x -= 1
                self.renderableEnemy.advanceStep()

            if (self.renderableEnemy.coordinates.x
                    == self.renderablePlayer.coordinates.x + 15):
                self.renderableEnemy.texture.changeAnimation(
                    CharacterAnimationType.standing, direction=Direction.none)
                self.myTimer.setTimer(2.0)
                self.state = IntroSceneState.speakenemy
                self.textureEmiter.showSpeechBubble(
                    'The princess is in another castle...',
                    time=3.0,
                    parentRenderable=self.renderableEnemy
                )

        elif self.state is IntroSceneState.speakenemy:
            if self.myTimer.timeIsUp():

                self.state = IntroSceneState.leaveenemy
                self.renderableEnemy.texture.changeAnimation(
                    CharacterAnimationType.walking, direction=Direction.right)
                self.myTimer.setTimer(0.1)

        elif self.state is IntroSceneState.leaveenemy:
            if self.myTimer.timeIsUp():
                self.myTimer.reset()
                self.renderableEnemy.advanceStep()
                self.renderableEnemy.coordinates.x += 1

            if (self.renderableEnemy.coordinates.x
                    == Config.columns):
                self.state = IntroSceneState.done


        elif self.state is IntroSceneState.done:
            pass
