import random
import logging

from ai.states import BaseState as State
from utilities.timer import Timer
from sprite.coordinates import Coordinates, ExtCoordinates
from utilities.utilities import Utility
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
import system.renderable
import system.gamelogic.enemy
from utilities.entityfinder import EntityFinder
from config import Config
import copy
from sprite.direction import Direction

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

        self.hitCd = [
            Coordinates(0, 0),
            Coordinates(1, 0),
            Coordinates(2, 0),
        ]
        self.hitCdWidth = 3
        self.hitCdHeight = 1


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        stateTimeRnd = random.randrange(-100 * meEnemy.enemyInfo.chaseTimeRnd, 100 * meEnemy.enemyInfo.chaseTimeRnd)
        self.setTimer(meEnemy.enemyInfo.chaseTime + (stateTimeRnd / 100))
        self.canAttackTimer.setTimer(meEnemy.enemyInfo.enemyCanAttackPeriod)
        self.canAttackTimer.reset()


    def process(self, dt):
        meAttackable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.attackable.Attackable)

        if meAttackable.isStunned:
            return

        didAttack = False

        self.lastInputTimer.advance(dt)
        self.canAttackTimer.advance(dt)

        # can attack player - based on playerlocation messages
        self.checkForNewPlayerPosition()
        if self.canAttackTimer.timeIsUp():
            if self.canAttackPlayer():
                if EntityFinder.numEnemiesInState(self.brain.owner.world, 'attack') < Config.enemiesInStateAttacking:
                    self.brain.pop()
                    self.brain.push("attackwindup")
                    didAttack = True

            self.canAttackTimer.reset()

        # note that if we want to attack, as identified a few lines above,
        # we will be in state attackWindup, and not reach here
        if didAttack:
            return

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
            self.brain.owner.entity, system.renderable.Renderable)

        if self.lastKnownPlayerPosition is None:
            # we may not yet have received a location.
            # find it directly via player entity
            # this is every time we go into chase state
            playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
            playerRenderable = self.brain.owner.world.component_for_entity(
                playerEntity, system.renderable.Renderable)
            self.lastKnownPlayerPosition = playerRenderable.getLocationAndSize()
        playerLocation = self.lastKnownPlayerPosition

        loc = meRenderable.getAttackBaseLocation()
        direction = meRenderable.getDirection()
        hitLocations = self.getHitLocations(loc, direction)

        # only one of the hitlocations need to hit
        for hitLocation in hitLocations:
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

        d1 = r1.coordinates.x - (r2.coordinates.x + r2.texture.width)
        d2 = (r1.coordinates.x + r1.texture.width) - r2.coordinats.x
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


    def getHitLocations(self, loc, direction):
        carr = copy.deepcopy(self.hitCd)

        for c in carr:
            c.x += loc.x
            c.y += loc.y
            if direction is Direction.left:
                c.x -= (self.hitCdWidth - 1)

        return carr


    def getInputChase(self):
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)

        if not Config.enemyMovement:
            return

        attackBaseLocation = meRenderable.getAttackBaseLocation()
        attackBaseLocationInverted = meRenderable.getAttackBaseLocationInverted()

        playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
        playerRenderable = self.brain.owner.world.component_for_entity(
            playerEntity, system.renderable.Renderable)
        playerLocation = playerRenderable.getLocation()

        moveX = 0
        moveY = 0
        dontChangeDirection = False

        if attackBaseLocation.x < playerLocation.x - 1:
            moveX = 1
        elif attackBaseLocation.x > playerLocation.x:  # + meEnemy.player.texture.width:
            moveX = -1

        # check if its better to just walk backwards
        distanceNormal = Utility.distance(playerLocation, attackBaseLocation)
        distanceInverted = Utility.distance(playerLocation, attackBaseLocationInverted)
        #logger.info("CC Dir: {}  X: {}   Normal: {}  Inverted: {}".format(
        #    meRenderable.direction, moveX,
        #    distanceNormal['sum'],
        #    distanceInverted['sum']
        #))
        if distanceNormal['sum'] < distanceInverted['sum']:
            dontChangeDirection = True

        # we can walk diagonally, no elif here
        if attackBaseLocation.y < playerLocation.y:
            moveY = 1
        elif attackBaseLocation.y > playerLocation.y + playerRenderable.texture.height - 1:  # why -1?
            moveY = -1

        # only move if we really move a character
        if moveX != 0 or moveY != 0:
            directMessaging.add(
                groupId = meGroupId.getId(),
                type = DirectMessageType.moveEnemy,
                data = {
                    'x': moveX,
                    'y': moveY,
                    'dontChangeDirection': dontChangeDirection
                },
            )
