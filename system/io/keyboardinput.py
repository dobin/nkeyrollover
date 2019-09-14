import logging

from messaging import messaging, MessageType
import system.singletons.gametime
from game.game import Game
from game.viewport import Viewport

logger = logging.getLogger(__name__)


class KeyboardInput(object):
    def __init__(self, game :Game):
        self.game :Game = game
        self.viewport :Viewport = game.viewport


    def getInput(self):
        gotInput = False
        key = self.viewport.win.getch()
        while key != -1:
            gotInput = True
            self.handleInput(key)
            key = self.viewport.win.getch()

        return gotInput


    def handleInput(self, key :str):
        # game related
        if key == ord('p'):
            self.game.togglePause()

        if key == 27:  # esc
            self.game.quitGame()

        if key == 265:  # f1
            self.game.toggleStats()

        if key == 266:  # f2
            pass

        messaging.add(
            type=MessageType.PlayerKeypress,
            data={
                'key': key,
                'time': system.singletons.gametime.getGameTime(),
            }
        )
