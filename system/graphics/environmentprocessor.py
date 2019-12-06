import logging
import esper

from game.viewport import Viewport
from messaging import messaging, MessageType
from system.singletons.environmentorchestrator import EnvironmentOrchestrator

logger = logging.getLogger(__name__)


class EnvironmentProcessor(esper.Processor):
    def __init__(
        self,
        viewport :Viewport,
        mapManager
    ):
        super().__init__()

        self.viewport :Viewport = viewport
        self.mapManager = mapManager

        self.environmentOrchestrator = EnvironmentOrchestrator(
            self.viewport, self.mapManager)


    def process(self, dt):
        self.checkMessages()


    def checkMessages(self):
        for message in messaging.getByType(MessageType.ScreenMove):
            self.trySpawn()

        for message in messaging.getByType(MessageType.GameStart):
            self.environmentOrchestrator.loadEnvironment()
            self.trySpawn()


    def trySpawn(self):
        # newX = message.data['x']
        newX = self.viewport.getx()

        self.environmentOrchestrator.trySpawn(self.world, newX)
        self.environmentOrchestrator.tryRemoveOld(self.world, newX)
