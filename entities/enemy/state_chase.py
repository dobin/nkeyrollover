import random
import logging

from ai.states import BaseState as State
from utilities.timer import Timer
from sprite.coordinates import Coordinates
from utilities.utilities import Utility
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessage, DirectMessageType
import system.renderable
import system.gamelogic.enemy
from utilities.entityfinder import EntityFinder
from config import Config
from utilities.entityfinder import EntityFinder

logger = logging.getLogger(__name__)


class StateChase(State):
    name = "chase"

    def __init__(self, brain):
        State.__init__(self, brain)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        self.lastInputTimer = Timer(
            meEnemy.enemyInfo.chaseStepDelay,
            instant=True )
        self.canAttackTimer = Timer()
        self.lastKnowsPlayerPosition = None


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        stateTimeRnd = random.randrange(-100 * meEnemy.enemyInfo.chaseTimeRnd, 100 * meEnemy.enemyInfo.chaseTimeRnd)
        self.setTimer( meEnemy.enemyInfo.chaseTime + (stateTimeRnd / 100) )
        self.canAttackTimer.setTimer(meEnemy.enemyInfo.enemyCanAttackPeriod)
        self.canAttackTimer.reset()


    def process(self, dt):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)
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
            self.lastKnowsPlayerPosition = message.data


    def canAttackPlayer(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        if self.lastKnowsPlayerPosition is None:
            # we may not yet have received a location. find it directly via player entity
            # this is every time we go into chase state
            playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
            playerRenderable = self.brain.owner.world.component_for_entity(
                playerEntity, system.renderable.Renderable)
            self.lastKnowsPlayerPosition = playerRenderable.getLocationAndSize()
        playerLocation = self.lastKnowsPlayerPosition

        attackRendable = self.brain.owner.world.component_for_entity(
            meEnemy.offensiveAttackEntity, system.renderable.Renderable)
        hitLocations = attackRendable.getTextureHitCoordinates()

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


    def getInputChase(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)

        if not meEnemy.enemyMovement:
            return

        meOffensiveWeaponRenderable = self.brain.owner.world.component_for_entity(
            meEnemy.offensiveAttackEntity, system.renderable.Renderable)
        meWeaponLocation = meOffensiveWeaponRenderable.getLocation()

        playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
        playerRenderable = self.brain.owner.world.component_for_entity(
            playerEntity, system.renderable.Renderable)
        playerLocation = playerRenderable.getLocation()

        moveX = 0
        moveY = 0
        dontChangeDirection = False

        if meWeaponLocation.x < playerLocation.x - 1:
            moveX = 1
        elif meWeaponLocation.x > playerLocation.x: #+ meEnemy.player.texture.width:
            moveX = -1

        # check if its better to just walk backwards
        meWeaponLocationInverted = meOffensiveWeaponRenderable.getLocationDirectionInverted()
        distanceNormal = Utility.distance(playerLocation, meWeaponLocation)
        distanceInverted = Utility.distance(playerLocation, meWeaponLocationInverted)
        #logger.info("CC Dir: {}  X: {}   Normal: {}  Inverted: {}".format(
        #    meRenderable.direction, moveX,
        #    distanceNormal['sum'],
        #    distanceInverted['sum']
        #))
        if distanceNormal['sum'] < distanceInverted['sum']:
            dontChangeDirection = True

        # we can walk diagonally, no elif here
        if meWeaponLocation.y < playerLocation.y:
            moveY = 1
        elif meWeaponLocation.y > playerLocation.y + playerRenderable.texture.height - 1: # why -1?
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
