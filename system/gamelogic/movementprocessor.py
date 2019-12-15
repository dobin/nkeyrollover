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
from system.graphics.particleeffecttype import ParticleEffectType

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

        for msg in directMessaging.getByType(DirectMessageType.movePlayer):
            # usually just one msg...
            playerGroupId = self.world.component_for_entity(
                playerEntity, system.groupid.GroupId)
            playerRenderable = self.world.component_for_entity(
                playerEntity, system.graphics.renderable.Renderable)

            x = msg.data['x']
            y = msg.data['y']
            dontChangeDirection = msg.data['dontChangeDirection']
            whenMoved = msg.data['whenMoved']

            # only turn, dont walk
            if not dontChangeDirection and Config.turnOnSpot:
                if playerRenderable.direction is Direction.left and x > 0:
                    self.updateRenderableDirection(
                        playerRenderable, Direction.right, playerGroupId.getId())
                    continue
                if playerRenderable.direction is Direction.right and x < 0:
                    self.updateRenderableDirection(
                        playerRenderable, Direction.left, playerGroupId.getId())
                    continue

            playerRenderable.storeCoords()
            playerRenderable.changeLocationFromStored(x, y)

            canMove = EntityFinder.isDestinationEmpty(
                self.world, playerRenderable)
            if not canMove:
                # try with one step, instead of the original two
                if x > 0:
                    x -= 1
                    playerRenderable.changeLocationFromStored(x, y)
                elif x < 0:
                    x += 1
                    playerRenderable.changeLocationFromStored(x, y)

                canMove = EntityFinder.isDestinationEmpty(
                    self.world, playerRenderable)
                if not canMove:
                    # we are stuck
                    playerRenderable.restoreCoords()
                    continue
                else:
                    # can move with new coordinates
                    pass

            playerRenderable.restoreCoords()

            didMove = self.moveRenderable(
                playerRenderable,
                playerGroupId.getId(),
                x,
                y,
                dontChangeDirection)

            if didMove:
                if whenMoved == "showAppearEffect":
                    locCenter = playerRenderable.getLocationCenter()
                    messaging.add(
                        type=MessageType.EmitMirageParticleEffect,
                        data= {
                            'location': locCenter,
                            'effectType': ParticleEffectType.appear,
                            'damage': 0,
                            'byPlayer': True,
                            'direction': Direction.none,
                        }
                    )
                if whenMoved == "showOnKnockback":
                    pass  # for now

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
            if entity is None:
                # May be already deleted?
                continue

            meRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            # these are the actual x/y position change we will use to move
            x = msg.data['x']
            y = msg.data['y']

            # turning on the spot
            if meRenderable.direction is Direction.left and x > 0:
                self.updateRenderableDirection(
                    meRenderable, Direction.right, msg.groupId)
                continue
            if meRenderable.direction is Direction.right and x < 0:
                self.updateRenderableDirection(
                    meRenderable, Direction.left, msg.groupId)
                continue

            meRenderable.storeCoords()
            meRenderable.changeLocationFromStored(x, y)

            if msg.data['force']:
                canMove = True

                # push player out of the way, if there
                isDestEmpty = EntityFinder.isDestinationEmpty(
                    self.world, meRenderable)
                if not isDestEmpty:
                    if EntityFinder.isDestinationWithPlayer(
                        self.world, meRenderable
                    ):
                        directMessaging.add(
                            groupId = 0,
                            type = DirectMessageType.movePlayer,
                            data = {
                                'x': x,
                                'y': 0,
                                'dontChangeDirection': True,
                                'whenMoved': None,
                            },
                        )

            else:
                canMove = EntityFinder.isDestinationEmpty(
                    self.world, meRenderable)

                if not canMove:
                    # seems we cannot move in the chose direction.
                    # if there are two components in the coordinates, just try one of
                    # them
                    if x != 0 and y != 0:
                        # try x. yes this is ugly, but fast
                        x = msg.data['x']
                        y = 0
                        meRenderable.changeLocationFromStored(x, y)
                        canMove = EntityFinder.isDestinationEmpty(
                            self.world, meRenderable)

                        if not canMove:
                            # try y... ugh
                            x = 0
                            y = msg.data['y']
                            meRenderable.changeLocationFromStored(x, y)
                            canMove = EntityFinder.isDestinationEmpty(
                                self.world, meRenderable)

                # check if we are stuck
                if not canMove:
                    meRenderable.restoreCoords()

                    isStuck = not EntityFinder.isDestinationEmpty(
                        self.world, meRenderable
                    )
                    if isStuck:
                        logger.info("{}: Overlaps, force way out".format(meRenderable))
                        # force our way out of here. do intended path
                        x = msg.data['x']
                        y = msg.data['y']
                        canMove = True
                    else:
                        # not stuck, just wait until we are free,
                        # as another enemy most likely blocks our way
                        logger.info("{}: Does not overlap, wait until moving".format(
                            meRenderable))
                        pass

            meRenderable.restoreCoords()

            if canMove:
                self.moveRenderable(
                    meRenderable,
                    msg.groupId,
                    x,
                    y,
                    msg.data['dontChangeDirection'],
                    msg.data['updateTexture'])


    def updateRenderableDirection(self, renderable, direction, groupId):
        renderable.setDirection(direction)

        # notify texture manager
        messaging.add(
            groupId = groupId,
            type = MessageType.EntityMoved,
            data = {
                'didChangeDirection': True,
                'x': 0,
                'y': 0,
            }
        )


    def moveRenderable(
        self, renderable, groupId, x :int =0, y :int =0,
        dontChangeDirection :bool =False,
        updateTexture :bool =True
    ) -> bool:
        """Move this renderable in x/y direction, if map allows. Update direction too"""
        didMove = False
        didChangeDirection = False

        if x > 0:
            if (renderable.canMoveOutsideMap
                    or renderable.coordinates.x + x < self.mapManager.getCurrentMapWidth()):
                renderable.coordinates.x += x
                didMove = True

                if (not dontChangeDirection
                        and renderable.direction is not Direction.right):
                    renderable.setDirection(Direction.right)
                    didChangeDirection = True

        elif x < 0:
            if (renderable.canMoveOutsideMap
                    or renderable.coordinates.x + x > 1):
                renderable.coordinates.x += x
                didMove = True
                if (not dontChangeDirection
                        and renderable.direction is not Direction.left):
                    renderable.setDirection(Direction.left)
                    didChangeDirection = True

        if y > 0:
            if (renderable.canMoveOutsideMap
                    or renderable.coordinates.y < Config.rows - renderable.texture.height - 1):
                renderable.coordinates.y += y
                didMove = True

        elif y < 0:
            if (renderable.canMoveOutsideMap
                    or renderable.coordinates.y > Config.areaMoveable['miny'] - renderable.texture.height + 1):
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
