import logging

from utilities.timer import Timer
from world.scenes.scenebase import SceneBase
from sprite.coordinates import Coordinates
from system.graphics.renderable import Renderable

from texture.phenomena.phenomenatype import PhenomenaType
from texture.phenomena.phenomenatexture import PhenomenaTexture
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class Scene3(SceneBase):
    def __init__(self, viewport, world):
        super().__init__(world=world)
        self.viewport = viewport
        self.name = "Scene2 - Map 0x01"
        self.isShowPlayer = True
        self.isShowMap = True      


    def enter(self):
        # spawn player
        messaging.add(
            type=MessageType.SpawnPlayer,
            data={},
        )

        # enable enemies
        pass


    def handlePosition(self, playerPosition, viewportX):
        pass


    def advance(self, dt): 
        pass