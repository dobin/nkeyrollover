import logging
import esper

from config import Config
from common.coordinates import ExtCoordinates
from common.direction import Direction
import system.gamelogic.attackable
import system.gamelogic.enemy
import system.gamelogic.player
import system.graphics.renderable
import system.groupid
from messaging import messaging, MessageType
from utilities.entityfinder import EntityFinder
from directmessaging import directMessaging, DirectMessageType
from game.mapmanager import MapManager

logger = logging.getLogger(__name__)


class MovementProcessor(esper.Processor):
    def __init__(self, mapManager :MapManager):
        super().__init__()
        self.mapManager :MapManager = mapManager


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

        for msg in directMessaging.getByType(DirectMessageType.movePlayer):
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


    def moveEnemy(self):
        for msg in directMessaging.getByType(DirectMessageType.moveEnemy):
            entity = EntityFinder.findCharacterByGroupId(self.world, msg.groupId)
            meRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            # coords to test if we can move to it
            # Note: same x/y calc like in self.moveRenderable()
            extCoords = meRenderable.getLocationAndSize()
            extCoords.x += msg.data['x']
            extCoords.y += msg.data['y']

            # these are the actual x/y position change we will use to move
            x = msg.data['x']
            y = msg.data['y']

            if msg.data['force']:
                canMove = True
            else:
                canMove = EntityFinder.isDestinationEmpty(
                    self.world, meRenderable, extCoords)

                if not canMove:
                    # seems we cannot move in the chose direction.
                    # if there are two components in the coordinates, just try one of
                    # them
                    if x != 0 and y != 0:
                        # try x. yes this is ugly, but fast
                        x = msg.data['x']
                        y = 0
                        extCoords.y -= msg.data['y']
                        canMove = EntityFinder.isDestinationEmpty(
                            self.world, meRenderable, extCoords)

                        if not canMove:
                            # try y... ugh
                            x = 0
                            y = msg.data['y']
                            extCoords.x -= msg.data['x']
                            extCoords.y += msg.data['y']
                            canMove = EntityFinder.isDestinationEmpty(
                                self.world, meRenderable, extCoords)

                # check if we are stuck
                if not canMove:
                    isStuck = not EntityFinder.isDestinationEmpty(
                        self.world, meRenderable, meRenderable.getLocationAndSize()
                    )
                    if isStuck:
                        # force our way out of here. do intended path
                        x = msg.data['x']
                        y = msg.data['y']
                        canMove = True
                    else:
                        # not stuck, just wait until we are free,
                        # as another enemy most likely blocks our way
                        pass

            if canMove:
                self.moveRenderable(
                    meRenderable,
                    msg.groupId,
                    x,
                    y,
                    msg.data['dontChangeDirection'],
                    msg.data['updateTexture'])


    def moveRenderable(
        self, renderable, groupId, x :int =0, y :int =0,
        dontChangeDirection :bool =False,
        updateTexture :bool =True
    ) -> bool:
        """Move this renderable in x/y direction, if map allows. Update direction too"""
        didMove = False
        didChangeDirection = False

        if x > 0:
            if renderable.coordinates.x + x < self.mapManager.getCurrentMapWidth():
                renderable.coordinates.x += x
                didMove = True

                if (not dontChangeDirection
                        and renderable.direction is not Direction.right):
                    renderable.setDirection(Direction.right)
                    didChangeDirection = True

        elif x < 0:
            if renderable.coordinates.x + x > 1:
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

        if updateTexture:
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
