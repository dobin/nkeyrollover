import logging
import esper

from config import Config
from common.coordinates import Coordinates, ExtCoordinates
from common.direction import Direction
import system.gamelogic.attackable
import system.gamelogic.enemy
import system.gamelogic.player
import system.graphics.renderable
import system.groupid
from messaging import messaging, MessageType
from utilities.utilities import Utility
from utilities.entityfinder import EntityFinder
from directmessaging import directMessaging, DirectMessageType

logger = logging.getLogger(__name__)


class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        self.movePlayer()
        self.moveEnemy()


    def movePlayer(self):
        playerEntity = EntityFinder.findPlayer(self.world)
        if playerEntity is None:
            return
        playerGroupId = self.world.component_for_entity(
            playerEntity, system.groupid.GroupId)
        playerRenderable = self.world.component_for_entity(
            playerEntity, system.graphics.renderable.Renderable)

        msg = directMessaging.get(
            messageType = DirectMessageType.movePlayer
        )
        while msg is not None:
            didMove = self.moveRenderable(
                playerRenderable,
                playerGroupId.getId(),
                msg.data['x'],
                msg.data['y'])

            if didMove:
                extcords = ExtCoordinates(
                    playerRenderable.coordinates.x,
                    playerRenderable.coordinates.y,
                    playerRenderable.texture.width,
                    playerRenderable.texture.height)
                messaging.add(
                    type = MessageType.PlayerLocation,
                    data = extcords)

            msg = directMessaging.get(
                messageType = DirectMessageType.movePlayer
            )

    def moveEnemy(self):
        msg = directMessaging.get(
            messageType = DirectMessageType.moveEnemy
        )
        while msg is not None:
            entity = EntityFinder.findCharacterByGroupId(self.world, msg.groupId)
            meRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)
            self.moveRenderable(
                meRenderable,
                msg.groupId,
                msg.data['x'],
                msg.data['y'],
                msg.data['dontChangeDirection'])

            msg = directMessaging.get(
                messageType = DirectMessageType.moveEnemy
            )


    def moveRenderable(
        self, renderable, groupId, x :int =0, y :int =0,
        dontChangeDirection :bool =False
    ):
        """Move this renderable in x/y direction, if allowed. Update direction too"""
        didMove = False
        didChangeDirection = False

        if x > 0:
            #if renderable.coordinates.x < Config.columns - renderable.texture.width - 1:
            if True:
                renderable.coordinates.x += x
                didMove = True

                if (not dontChangeDirection
                        and renderable.direction is not Direction.right):
                    renderable.setDirection(Direction.right)
                    didChangeDirection = True

        elif x < 0:
            if renderable.coordinates.x > 1:
                renderable.coordinates.x += x
                didMove = True
                if (not dontChangeDirection
                        and renderable.direction is not Direction.left):
                    renderable.setDirection(Direction.left)
                    didChangeDirection = True

        if y > 0:
            if renderable.coordinates.y < Config.rows - renderable.texture.height - 1:
                renderable.coordinates.y += y
                didMove = True

        elif y < 0:
            if (renderable.coordinates.y
                    > Config.areaMoveable['miny'] - renderable.texture.height + 1):
                renderable.coordinates.y += y
                didMove = True

        # notify texture manager
        messaging.add(
            groupId = groupId,
            type = MessageType.EntityMoved,
            data = {
                'didChangeDirection': didChangeDirection,
                'x': x,
                'y': y,
            }
        )

        return didMove
