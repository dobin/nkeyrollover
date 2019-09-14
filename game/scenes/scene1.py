import logging
import curses
from enum import Enum

from utilities.timer import Timer
from game.scenes.scenebase import SceneBase
from common.coordinates import Coordinates
from system.graphics.renderable import Renderable

from texture.phenomena.phenomenatype import PhenomenaType
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.character.characteranimationtype import CharacterAnimationType
from texture.character.charactertexture import CharacterTexture
from texture.character.charactertexturetype import CharacterTextureType

logger = logging.getLogger(__name__)


class IntroSceneState(Enum):
    wait1 = 1       # wait 1s
    flydown = 2     # fly heli down
    drop = 3        # drop asciiman
    flyup = 4       # fly up
    done = 5        # start the game



class Scene1(SceneBase):
    def __init__(self, viewport, world):
        super().__init__(world=world, viewport=viewport)

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
            active=False,
        )

        self.renderableCopter = renderableCopter
        self.renderablePlayer = renderablePlayer

        self.myTimer = Timer(0.5)
        self.state = IntroSceneState.wait1
        self.name = "Scene1 - Intro Animation"
        self.anyKeyFinishesScene = True


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
        if self.state is IntroSceneState.wait1 or self.state is IntroSceneState.flydown or self.state is IntroSceneState.drop or self.state is IntroSceneState.flyup:
            self.viewport.addstr(5, 40,  "N Key Rollover", curses.color_pair(5))
            self.viewport.addstr(6, 40,  "Adventures of ASCIIMAN", curses.color_pair(5))
            self.viewport.addstr(8, 40,  "Select attack: 1 2 3 4", curses.color_pair(1))
            self.viewport.addstr(9, 40,  "Attack       : space", curses.color_pair(1))
            self.viewport.addstr(10, 40, "Skills       : q w e r", curses.color_pair(1))
            self.viewport.addstr(11, 40, "Heal, Port   : f g", curses.color_pair(1))

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
                self.state = IntroSceneState.drop
                self.addRenderable(self.renderablePlayer)

        elif self.state is IntroSceneState.drop:
            # for next scene: Flyup
            if self.myTimer.timeIsUp():
                self.myTimer.reset()
                self.renderableCopter.coordinates.y -= 1

            if self.renderableCopter.coordinates.y == self.copterSpawn.y:
                self.state = IntroSceneState.done

        elif self.state is IntroSceneState.done:
            pass
