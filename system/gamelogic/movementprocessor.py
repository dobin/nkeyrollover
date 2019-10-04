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

            # Note: same x/y calc like in self.moveRenderable()
            extCoords = meRenderable.getLocationAndSize()
            extCoords.x += msg.data['x']
            extCoords.y += msg.data['y']

            if self.isDestinationEmpty(meRenderable, extCoords):
                self.moveRenderable(
                    meRenderable,
                    msg.groupId,
                    msg.data['x'],
                    msg.data['y'],
                    msg.data['dontChangeDirection'],
                    msg.data['updateTexture'])


    def isDestinationEmpty(self, renderable, extCoords :ExtCoordinates) -> bool:
        """Check if renderable/extCoords overlaps with any other renderables"""
        for ent, otherRend in self.world.get_component(system.graphics.renderable.Renderable):
            dist = otherRend.distanceToBorder(extCoords)
            if dist['x'] <= 0 and dist['y'] <= 0:
                if not renderable == otherRend:
                    return False

        return True


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
