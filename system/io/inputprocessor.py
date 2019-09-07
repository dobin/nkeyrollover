import esper
import curses
import logging

from utilities.timer import Timer
from messaging import messaging, MessageType
from config import Config
import system.graphics.renderable
import system.gamelogic.player
import system.gamelogic.attackable
from directmessaging import directMessaging, DirectMessageType
from utilities.apm import Apm
from utilities.entityfinder import EntityFinder

logger = logging.getLogger(__name__)


class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.movementTimer = Timer(1.0 / Config.movementKeysPerSec, instant=True)
        self.apm = Apm()


    def process(self, deltaTime):
        self.handleKeyboardInput()
        self.advance(deltaTime)


    def advance(self, deltaTime):
        self.movementTimer.advance(deltaTime)


    def handleKeyboardInput(self):
        playerEntity = EntityFinder.findPlayer(self.world)
        if playerEntity is None: 
            return

        player = self.world.component_for_entity(
                playerEntity, system.gamelogic.player.Player)
        renderable = self.world.component_for_entity(
                playerEntity, system.graphics.renderable.Renderable)
        attackable = self.world.component_for_entity(
                playerEntity, system.gamelogic.attackable.Attackable)

        didMove = False
        if attackable.isStunned:
            return
        if player.isAttacking:
            return

        for message in messaging.getByType(MessageType.PlayerKeypress):
            self.apm.tick(message.data['time'])
            didMoveTmp = self.handleKeyPress(
                message.data['key'], player, renderable, playerEntity)
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
                x = -1
                didMove = True

            elif key == curses.KEY_RIGHT:
                x = 1
                didMove = True

            elif key == curses.KEY_UP:
                y = -1
                didMove = True

            elif key == curses.KEY_DOWN:
                y = 1
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


