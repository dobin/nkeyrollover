import logging
from enum import Enum
import esper

from messaging import messaging, MessageType
from config import Config
import system.gamelogic.ai
import system.graphics.renderable

logger = logging.getLogger(__name__)


class State(Enum): 
    pushToNextScene = 0
    pushToEnemies = 1
    brawl = 2


class SceneProcessor(esper.Processor):
    def __init__(self, viewport, sceneManager):
        super().__init__()
        self.viewport = viewport
        self.sceneManager = sceneManager
        self.sceneManager.initScene()  # start first scene
        self.xCenter = Config.columns / 2 - 5
        self.state = None


    def numEnemiesAlive(self) -> int:
        count = 0
        for _, ai in self.world.get_component(system.gamelogic.ai.Ai):
            count += 1

        return count


    def numEnemiesVisible(self) -> int:
        count = 0
        for _, (ai, renderable) in self.world.get_components(
                system.gamelogic.ai.Ai, system.graphics.renderable.Renderable):
            if renderable.coordinates.x > self.viewport.getx() and renderable.coordinates.x < self.viewport.getRightX():
                count += 1

        return count


    def setState(self, state):
        if self.state != state:
            logger.warning("State: {}".format(state))
            self.state = state


    def process(self, dt):
        if self.numEnemiesAlive() == 0:
            self.setState(State.pushToNextScene)
        elif self.numEnemiesVisible() == 0:
            self.setState(State.pushToEnemies)
        else:
            self.setState(State.brawl)


        for message in messaging.getByType(MessageType.PlayerLocation):
            playerScreenCoords = self.viewport.getScreenCoords(
                message.data)

            if self.state is State.pushToNextScene:
                if playerScreenCoords.x != 10:
                    distance = int(playerScreenCoords.x - 10)
                    if distance > 0:
                        self.viewport.adjustViewport(1)

            elif self.state is State.pushToNextScene:
                # check if player is in center of screen (probably not, as he changed pos)
                if playerScreenCoords.x != self.xCenter:
                    distance = int(playerScreenCoords.x - self.xCenter)
                    if distance > 0:  # adjust here if we have levels in opposite direction
                        self.viewport.adjustViewport(1)

            elif self.state is State.brawl:
                # Close to border right
                if playerScreenCoords.x >= Config.moveBorderRight:
                    distance = playerScreenCoords.x - Config.moveBorderRight
                    self.viewport.adjustViewport(distance)
                if playerScreenCoords.x <= Config.moveBorderLeft:
                    distance = playerScreenCoords.x - Config.moveBorderLeft
                    self.viewport.adjustViewport(distance)

            # Check if we reached new
            self.sceneManager.handlePosition(message.data, self.viewport.getx())

        for message in messaging.getByType(MessageType.PlayerKeypress):
            self.sceneManager.handlePlayerKeyPress()

        self.sceneManager.advance(dt)
