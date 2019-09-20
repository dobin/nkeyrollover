import logging

from utilities.timer import Timer
from game.scenes.scenebase import SceneBase
from common.coordinates import Coordinates
from system.graphics.renderable import Renderable

from texture.phenomena.phenomenatype import PhenomenaType
from texture.phenomena.phenomenatexture import PhenomenaTexture

logger = logging.getLogger(__name__)


class SceneLogo(SceneBase):
    def __init__(self, viewport, world):
        super().__init__(world=world, viewport=viewport)

        # teh logo
        coordinates = Coordinates(2, 5)
        textureLogo = PhenomenaTexture(
            phenomenaType=PhenomenaType.intro)
        self.renderableLogo = Renderable(
            texture=textureLogo,
            viewport=self.viewport,
            coordinates=coordinates,
            active=True,
        )

        self.anyKeyFinishesScene = True

        self.timer = Timer(3)
        self.sceneFinished = False
        self.name = "Scene0 - Logo"


    def enter(self):
        self.addRenderable(self.renderableLogo)


    def sceneIsFinished(self):
        if self.timer.timeIsUp():
            return True
        else:
            return False


    def advance(self, dt):
        self.timer.advance(dt)
