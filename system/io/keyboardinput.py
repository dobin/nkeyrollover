import logging
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent

from messaging import messaging, MessageType
import system.singletons.gametime
from game.game import Game
from game.viewport import Viewport

logger = logging.getLogger(__name__)


class KeyboardInput(object):
    def __init__(self, game :Game, viewport :Viewport):
        self.game :Game = game
        self.viewport :Viewport = viewport


    def getInput(self):
        gotInput = False
        event = self.viewport.win.get_event()
        while event is not None:
            if type(event) is KeyboardEvent:
                gotInput = True
                self.handleInput(event.key_code)
            event = self.viewport.win.get_event()

        return gotInput


    def handleInput(self, key :str):
        # game related
        if key == ord('p'):
            self.game.togglePause()

        if key == Screen.KEY_ESCAPE:  # esc
            self.game.quitGame()

        if key == Screen.KEY_F1:  # f1
            self.game.toggleStats()

        if key == Screen.KEY_F2:  # f2
            self.game.toggleLog()

        messaging.add(
            type=MessageType.PlayerKeypress,
            data={
                'key': key,
                'time': system.singletons.gametime.getGameTime(),
            }
        )
