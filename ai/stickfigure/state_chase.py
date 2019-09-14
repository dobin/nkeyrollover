import random
import logging

from common.direction import Direction
from stackfsm.states import BaseState as State
from utilities.timer import Timer
from common.coordinates import Coordinates
from utilities.utilities import Utility
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
import system.graphics.renderable
import system.gamelogic.enemy
from utilities.entityfinder import EntityFinder
from config import Config
import copy
from utilities.color import Color


logger = logging.getLogger(__name__)


class StateChase(State):
    name = "chase"

    def __init__(self, brain):
        State.__init__(self, brain)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        self.lastInputTimer = Timer(
            meEnemy.enemyInfo.chaseStepDelay,
            instant=True)
        self.canAttackTimer = Timer()
        self.lastKnownPlayerPosition = None


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        stateTimeRnd = random.randrange(
            -100 * meEnemy.enemyInfo.chaseTimeRnd,
            100 * meEnemy.enemyInfo.chaseTimeRnd)
        self.setTimer(meEnemy.enemyInfo.chaseTime + (stateTimeRnd / 100))
        self.canAttackTimer.setTimer(meEnemy.enemyInfo.enemyCanAttackPeriod)
        self.canAttackTimer.reset()


    def process(self, dt):
        meAttackable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.attackable.Attackable)

        if meAttackable.isStunned:
            return

        self.lastInputTimer.advance(dt)
        self.canAttackTimer.advance(dt)

        # can attack player - based on playerlocation messages
        self.checkForNewPlayerPosition()
        if self.canAttackTimer.timeIsUp():
            if self.canAttackPlayer():
                if (EntityFinder.numEnemiesInState(self.brain.owner.world, 'attack') 
                        < Config.enemiesInStateAttacking):
                    self.brain.pop()
                    self.brain.push("attackwindup")
                    pass

            self.canAttackTimer.reset()

        # note that if we want to attack, as identified a few lines above,
        # we will be in state attackWindup, and not reach here

        # only move if we can not hit him (even on cooldown)
        # if not self.canAttackPlayer():
        if True:
            # movement speed, and direction
            if self.lastInputTimer.timeIsUp():
                self.getInputChase()
                self.lastInputTimer.reset()

        # switch to wander if exhausted
        if self.timeIsUp():
            logger.debug("{}: Too long chasing, switching to wander".format(self.owner))
            self.brain.pop()
            self.brain.push("wander")


    def checkForNewPlayerPosition(self):
        # check if there are any new player position messages
        for message in messaging.getByType(MessageType.PlayerLocation):
            self.lastKnownPlayerPosition = message.data


    def canAttackPlayer(self):
        logging.info("{}: (slow) Check if i can attack player".format(self.name))
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.graphics.renderable.Renderable)
        meOffensiveAttack = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.offensiveattack.OffensiveAttack)

        if self.lastKnownPlayerPosition is None:
            # we may not yet have received a location.
            # find it directly via player entity
            # this is every time we go into chase state
            playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
            playerRenderable = self.brain.owner.world.component_for_entity(
                playerEntity, system.graphics.renderable.Renderable)
            self.lastKnownPlayerPosition = playerRenderable.getLocationAndSize()
        playerLocation = self.lastKnownPlayerPosition

        loc = meRenderable.getWeaponBaseLocation()
        direction = meRenderable.getDirection()
        currentWeaponHitArea = meOffensiveAttack.getCurrentWeaponHitArea()
        self.updateWeaponHitArea(
            currentWeaponHitArea,
            loc,
            direction)

        if Config.showEnemyHitbox:
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
            canAttack = Utility.pointIn(
                hitLocation,
                playerLocation)

            if canAttack:
                logger.info("{} Can attack, me {} in {}".format(
                    self.name, hitLocation, playerLocation
                ))
                return True

        return False


    def distance(self, r1, r2):
        res = {
            'x': 0,
            'y': 0,
        }

        d1 = r1.coordinates.x - (r2.coordinates.x + r2.texture.width - 1)
        d2 = (r1.coordinates.x + r1.texture.width - 1) - r2.coordinats.x
        if d1 < d2:
            res['x'] = d1
        elif d1 > d2:
            res['x'] = d2

        d1 = r1.coordinates.y - (r2.coordinates.y + r2.texture.height)
        d2 = (r1.coordinates.y + r1.texture.height) - r2.coordinats.y
        if d1 < d2:
            res['y'] = d1
        elif d1 > d2:
            res['y'] = d2

        return res


    def updateWeaponHitArea(self, weaponHitArea, loc, direction):
        carr = weaponHitArea.hitCd
        for c in carr:
            c.x += loc.x
            c.y += loc.y
            if direction is Direction.left:
                c.x -= (weaponHitArea.width - 1)
        #return carr


    def getInputChase(self):
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.graphics.renderable.Renderable)

        if not Config.enemyMovement:
            return

        # enemy will walk to this distance
        # allows player to come close
        # but not inside of him, will walk backwards
        keepDistance = 1

        attackBaseLocation = meRenderable.getAttackBaseLocation()
        attackBaseLocationInverted = meRenderable.getAttackBaseLocationInverted()

        playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
        plyrRend = self.brain.owner.world.component_for_entity(
            playerEntity, system.graphics.renderable.Renderable)
        playerLocation = plyrRend.getLocation()

        # check distance, from both the direction we are facing, 
        # and the other one
        distanceNormal = Utility.distance(playerLocation, attackBaseLocation)
        distanceInverted = Utility.distance(playerLocation, attackBaseLocationInverted)

        # logging.info("--- Loc Enemy : {} / {}".format(
        #     meRenderable.coordinates.x, 
        #     meRenderable.coordinates.x + meRenderable.texture.width - 1))
        # logging.info("--- Loc Player: {}".format(playerRenderable.coordinates.x))

        # decide on which reference point we will take
        # and if we wanna change direction
        atkLoc = None
        dontChangeDirection = False
        if distanceNormal['x'] < distanceInverted['x']:
            # logging.info("--- n: {}  i: {}   dontChange, use normal".format(
            #     distanceNormal['x'], distanceInverted['x']
            # ))
            dontChangeDirection = True
            atkLoc = attackBaseLocation
        else:
            # logging.info("--- n: {}  i: {}   change, use inverted".format(
            #     distanceNormal['x'], distanceInverted['x']
            # ))
            dontChangeDirection = False
            atkLoc = attackBaseLocationInverted

        # logging.info("--- Loc Atk    : {}".format(attackLoc.x))

        moveX = 0
        moveY = 0
        # check if player overlaps with out attackpoint
        # if yes, we are too close
        if (atkLoc.x >= plyrRend.coordinates.x
                and atkLoc.x <= plyrRend.coordinates.x + plyrRend.texture.width - 1):
            # logging.info("--- Overlap :-(")
            # if refLoc.x >= playerRenderable.coordinates.x:
            if meRenderable.direction is Direction.left:
                moveX = 1
            else:
                moveX = -1

            # logging.info("--- Overlap decision: {}".format(moveX))

        else:
            # logging.info("--- No overlap :-)")

            playerref = 0
            if atkLoc.x <= playerLocation.x + int(plyrRend.texture.width / 2):
                # logging.info("--- Enemy is left of player")
                playerref = playerLocation.x
            else:
                # logging.info("--- Enemy is right of player. Ex:{} Px:{}".format(
                #     attackLoc.x, playerRenderable.coordinates.x
                # ))
                playerref = playerLocation.x + plyrRend.texture.width - 1

            tempDistance = atkLoc.x - playerref
            if tempDistance > keepDistance:
                moveX = -1
            elif tempDistance < -keepDistance:
                moveX = 1

            # logging.info("--- Distance: {} because {} - {} ".format(
            #     tempDistance, attackLoc.x, playerref))

            # logging.info("--- Enemy: moveX: {} dontChangeDirection: {}".format(
            #     moveX, dontChangeDirection
            # ))

        # we can walk diagonally, no elif here
        if attackBaseLocation.y < playerLocation.y:
            moveY = 1
        elif attackBaseLocation.y > playerLocation.y + plyrRend.texture.height - 1:
            moveY = -1

        # only move if we really move a character
        if moveX != 0 or moveY != 0:
            directMessaging.add(
                groupId = meGroupId.getId(),
                type = DirectMessageType.moveEnemy,
                data = {
                    'x': moveX,
                    'y': moveY,
                    'dontChangeDirection': dontChangeDirection,
                    'updateTexture': True
                },
            )
