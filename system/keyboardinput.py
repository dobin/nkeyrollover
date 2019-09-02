import logging

from system.gamelogic.player import Player
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class KeyboardInput(object):
    def __init__(self, world): 
        self.world = world
        self.viewport = world.viewport


    def getInput(self):
        gotInput = False
        key = self.viewport.win.getch()
        while key != -1:
            gotInput = True
            self.handleInput(key)
            key = self.viewport.win.getch()

        return gotInput


    def handleInput(self, key):
            # game related
            if key == ord('p'):
                self.world.togglePause()

            if key == 27: # esc
                self.world.quitGame()

            if key == 265: # f1
                self.world.toggleStats()

            if key == 266: # f2
                self.world.toggleShowEnemyWanderDestination()                

            messaging.add(
                type=MessageType.PlayerKeypress, 
                data=key)

            player = self.world.esperWorld.component_for_entity(self.world.player, Player)
            player.characterStatus.handleKeyPress(time=self.world.getGameTime())



    def advance(self, deltaTime):
        pass
