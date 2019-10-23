import esper
import logging
from asciimatics.screen import Screen

from utilities.timer import Timer
from messaging import messaging, MessageType
from config import Config
import system.graphics.renderable
import system.gamelogic.player
import system.gamelogic.attackable
from directmessaging import directMessaging, DirectMessageType
from system.singletons.apm import apm
from utilities.entityfinder import EntityFinder

logger = logging.getLogger(__name__)


class InputProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.movementTimer = Timer(1.0 / Config.movementKeysPerSec, instant=True)


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
            if not player.isAlive:
                messaging.add(
                    type = MessageType.GameRestart,
                    data = {},
                )
                message.type = MessageType.Deleted
                return

            apm.tick(message.data['time'])
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
            dontChangeDirection = False

            if key == Screen.KEY_LEFT:
                if Config.xDoubleStep:
                    x = -2
                else:
                    x = -1
                didMove = True

            elif key == Screen.KEY_RIGHT:
                if Config.xDoubleStep:
                    x = 2
                else:
                    x = 1
                didMove = True

            if key == 393:  # shift left
                dontChangeDirection = True
                if Config.xDoubleStep:
                    x = -2
                else:
                    x = -1
                didMove = True

            elif key == Screen.KEY_RIGHT:
                if Config.xDoubleStep:
                    x = 2
                else:
                    x = 1
                didMove = True

            if key == 402:  # shift right
                dontChangeDirection = True
                if Config.xDoubleStep:
                    x = 2
                else:
                    x = 1
                didMove = True

            elif key == Screen.KEY_UP:
                y = -1
                didMove = True

            elif key == Screen.KEY_DOWN:
                y = 1
                didMove = True

        meGroupId = self.world.component_for_entity(
            playerEntity, system.groupid.GroupId)

        if didMove:
            directMessaging.add(
                groupId = meGroupId.getId(),
                type = DirectMessageType.movePlayer,
                data = {
                    'x': x,
                    'y': y,
                    'dontChangeDirection': dontChangeDirection,
                    'whenMoved': None,
                },
            )

        return didMove
