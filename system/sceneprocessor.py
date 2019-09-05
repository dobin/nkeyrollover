import logging
import esper

from messaging import messaging, Messaging, Message, MessageType
from config import Config
from directmessaging import directMessaging, DirectMessageType
import system.gamelogic.attackable
import system.gamelogic.enemy
import system.gamelogic.player
import system.renderable
import system.groupid

logger = logging.getLogger(__name__)


class SceneProcessor(esper.Processor):
    def __init__(self, viewport, sceneManager):
        super().__init__()
        self.viewport = viewport
        self.sceneManager = sceneManager
        self.sceneManager.initScene() # start first scene


    def process(self, dt):
        for message in messaging.getByType(MessageType.PlayerLocation):
            # Check if we need to scroll the window
            playerScreenCoords = self.viewport.getScreenCoords (
                message.data )
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