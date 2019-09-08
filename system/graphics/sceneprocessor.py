import logging
import esper

from messaging import messaging, MessageType
from config import Config

logger = logging.getLogger(__name__)


class SceneProcessor(esper.Processor):
    def __init__(self, viewport, sceneManager):
        super().__init__()
        self.viewport = viewport
        self.sceneManager = sceneManager
        self.sceneManager.initScene()  # start first scene


    def process(self, dt):
        for message in messaging.getByType(MessageType.PlayerLocation):
            # Check if we need to scroll the window
            playerScreenCoords = self.viewport.getScreenCoords(
                message.data)
            if playerScreenCoords.x >= Config.moveBorderRight:
                distance = playerScreenCoords.x - Config.moveBorderRight
                self.viewport.adjustViewport(distance)
            if playerScreenCoords.x <= Config.moveBorderLeft:
                distance = playerScreenCoords.x - Config.moveBorderLeft
                self.viewport.adjustViewport(-1)

            # Check if we reached new
            self.sceneManager.handlePosition(message.data, self.viewport.getx())

        for message in messaging.getByType(MessageType.PlayerKeypress):
            self.sceneManager.handlePlayerKeyPress()

        self.sceneManager.advance(dt)