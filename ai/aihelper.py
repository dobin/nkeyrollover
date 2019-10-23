import logging
import random

from utilities.utilities import Utility
from common.direction import Direction
from common.coordinates import Coordinates
from utilities.color import Color
from config import Config
from messaging import messaging, MessageType
from utilities.entityfinder import EntityFinder
import system.graphics.renderable
import system.gamelogic.enemy

logger = logging.getLogger(__name__)


class AiHelper(object):
    @staticmethod
    def canAttackPlayer(owner, playerLocation):
        if playerLocation is None:
            return False

        meRenderable = owner.world.component_for_entity(
            owner.entity, system.graphics.renderable.Renderable)
        meOffensiveAttack = owner.world.component_for_entity(
            owner.entity, system.gamelogic.offensiveattack.OffensiveAttack)

        currentWeaponHitArea = meOffensiveAttack.getCurrentWeaponHitArea()

        if Config.showEnemyWeaponHitCollisionDetectionTargets:
            for hitlocation in currentWeaponHitArea.hitCd:
                messaging.add(
                    type=MessageType.EmitTextureMinimal,
                    data={
                        'char': 'X',
                        'timeout': 0.2,
                        'coordinate': hitlocation,
                        'color': Color.grey
                    }
                )

        # only one of the hitlocations need to hit
        for hitLocation in currentWeaponHitArea.hitCd:
            canAttack = Utility.isPointInArea(
                hitLocation,
                playerLocation)
            if canAttack:
                return True
        return False


    @staticmethod
    def getAttackVectorToPlayer(owner, meRenderable):
        # enemy will walk to this distance
        # allows player to come close
        # but not inside of him, will walk backwards
        keepDistance = 1

        attackBaseLocation = meRenderable.getAttackBaseLocation()
        attackBaseLocationInverted = meRenderable.getAttackBaseLocationInverted()

        playerEntity = EntityFinder.findPlayer(owner.world)
        # player not spawned
        if not playerEntity:
            return

        plyrRend = owner.world.component_for_entity(
            playerEntity, system.graphics.renderable.Renderable)
        playerLocation = plyrRend.getLocation()

        # check distance, from both the direction we are facing, 
        # and the other one
        distanceNormal = Utility.distance(playerLocation, attackBaseLocation)
        distanceInverted = Utility.distance(playerLocation, attackBaseLocationInverted)

        # logger.info("--- Loc Enemy : {} / {}".format(
        #     meRenderable.coordinates.x, 
        #     meRenderable.coordinates.x + meRenderable.texture.width - 1))
        # logger.info("--- Loc Player: {}".format(playerRenderable.coordinates.x))

        # decide on which reference point we will take
        # and if we wanna change direction
        atkLoc = None
        dontChangeDirection = False
        if distanceNormal['x'] < distanceInverted['x']:
            # logger.info("--- n: {}  i: {}   dontChange, use normal".format(
            #     distanceNormal['x'], distanceInverted['x']
            # ))
            dontChangeDirection = True
            atkLoc = attackBaseLocation
        else:
            # logger.info("--- n: {}  i: {}   change, use inverted".format(
            #     distanceNormal['x'], distanceInverted['x']
            # ))
            dontChangeDirection = False
            atkLoc = attackBaseLocationInverted

        # logger.info("--- Loc Atk    : {}".format(attackLoc.x))

        moveX = 0
        moveY = 0
        # check if player overlaps with out attackpoint
        # if yes, we are too close
        if (atkLoc.x >= plyrRend.coordinates.x
                and atkLoc.x <= plyrRend.coordinates.x + plyrRend.texture.width - 1):
            # logger.info("--- Overlap :-(")
            # if refLoc.x >= playerRenderable.coordinates.x:
            if meRenderable.direction is Direction.left:
                if Config.xDoubleStep:
                    moveX = 2
                else:
                    moveX = 1
            else:
                if Config.xDoubleStep:
                    moveX = -2
                else:
                    moveX = -1

            # logger.info("--- Overlap decision: {}".format(moveX))

        else:
            # logger.info("--- No overlap :-)")

            playerref = 0
            if atkLoc.x <= playerLocation.x + int(plyrRend.texture.width / 2):
                # logger.info("--- Enemy is left of player")
                playerref = playerLocation.x
            else:
                # logger.info("--- Enemy is right of player. Ex:{} Px:{}".format(
                #     attackLoc.x, playerRenderable.coordinates.x
                # ))
                playerref = playerLocation.x + plyrRend.texture.width - 1

            tempDistance = atkLoc.x - playerref
            if tempDistance > keepDistance:
                if Config.xDoubleStep:
                    moveX = -2
                else:
                    moveX = -1
            elif tempDistance < -keepDistance:
                if Config.xDoubleStep:
                    moveX = 2
                else:
                    moveX = 1

            # logger.info("--- Distance: {} because {} - {} ".format(
            #     tempDistance, attackLoc.x, playerref))

            # logger.info("--- Enemy: moveX: {} dontChangeDirection: {}".format(
            #     moveX, dontChangeDirection
            # ))

        # we can walk diagonally, no elif here
        if attackBaseLocation.y < playerLocation.y:
            moveY = 1
        elif attackBaseLocation.y > playerLocation.y + plyrRend.texture.height - 1:
            moveY = -1

        return moveX, moveY, dontChangeDirection


    @staticmethod
    def getVectorToPlayer(source, dest):
        x = 0
        y = 0
        if dest.x > source.x:
            if Config.xDoubleStep:
                x = 2
            else:
                x = 1
        elif dest.x < source.x:
            if Config.xDoubleStep:
                x = -2
            else:
                x = -1

        if dest.y > source.y:
            y = 1
        elif dest.y < source.y:
            y = -1

        return x, y


    @staticmethod
    def pickDestAroundPlayer(meRenderable, distanceX, distanceY):
        ptRight = random.choice([True, False])
        ptDown = random.choice([True, False])

        coord = Coordinates(
            meRenderable.getLocation().x,
            meRenderable.getLocation().y
        )

        if ptRight:
            coord.x += distanceX + random.randint(2, 6)
        else:
            coord.x -= distanceX + random.randint(2, 6)

        if ptDown:
            coord.y += distanceY + random.randint(-2, 2)
            #if coord.y > Config.rows - 2 - meRenderable.texture.height:
            #    coord.y = Config.rows - 2 - meRenderable.texture.height
        else:
            coord.y -= distanceY + random.randint(-2, 2)
            # +1 so they can overlap only a bit on top
            #if coord.y < Config.topborder - meRenderable.texture.height + 1:
            #    coord.y = Config.topborder - meRenderable.texture.height + 1

        # make sure destination is on-screen
        if coord.y < Config.topborder:
            coord.y = Config.topborder
        if coord.y > Config.rows + meRenderable.texture.height:
            coord.y = Config.rows + meRenderable.texture.height

        return coord
