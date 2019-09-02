import esper
import curses
import logging
from enum import Enum

from utilities.timer import Timer
from messaging import messaging, Messaging, Message, MessageType
from config import Config
import system.advanceable 
import system.renderable
import system.gamelogic.player
from directmessaging import directMessaging, DirectMessage, DirectMessageType

logger = logging.getLogger(__name__)


class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.movementTimer = Timer( 1.0 / Config.movementKeysPerSec, instant=True)


    def process(self, deltaTime):
        self.handleKeyboardInput()
        self.advance(deltaTime)


    def advance(self, deltaTime):
        self.movementTimer.advance(deltaTime)


    def handleKeyboardInput(self):
        for ent, (renderable, player) in self.world.get_components(
            system.renderable.Renderable, system.gamelogic.player.Player
        ):
            didMove = False
            
            for message in messaging.get():
                if message.type is MessageType.PlayerKeypress:
                    didMoveTmp = self.handleKeyPress(message.data, player, renderable, ent)
                    if didMoveTmp: 
                        didMove = True

            # to allow diagonal movement, we allow multiple movement keys per input
            # cycle, without resetting the timer.
            if didMove: 
                self.movementTimer.reset()


    def handleKeyPress(self, key, player, playerRenderable, playerEntity):
        didMove = False
        x = 0
        y = 0
        if self.movementTimer.timeIsUp(): 
            if key == curses.KEY_LEFT:
                x=-1
                didMove = True

            elif key == curses.KEY_RIGHT: 
                x=1
                didMove = True

            elif key == curses.KEY_UP:
                y=-1
                didMove = True

            elif key == curses.KEY_DOWN: 
                y=1
                didMove = True

        meGroupId = self.world.component_for_entity(
            playerEntity, system.groupid.GroupId)
        directMessaging.add(
            groupId = meGroupId.getId(),
            type = DirectMessageType.movePlayer,
            data = {
                'x': x,
                'y': y
            },
        )

        return didMove


