import random
import logging

from ai.brain import Brain
from ai.states import BaseState as State
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from sprite.direction import Direction
from config import Config
from sprite.coordinates import Coordinates
from utilities.utilities import Utility
from utilities.color import Color
from messaging import messaging, Messaging, Message, MessageType

import system.renderable
import system.gamelogic.enemy

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


    def on_enter(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy) 

        stateTimeRnd = random.randrange(-100 * meEnemy.enemyInfo.chaseTimeRnd, 100 * meEnemy.enemyInfo.chaseTimeRnd)
        self.setTimer( meEnemy.enemyInfo.chaseTime + (stateTimeRnd / 100) )
        meRenderable.texture.changeAnimation(
            CharacterAnimationType.walking, 
            meRenderable.direction)
        self.canAttackTimer.setTimer(meEnemy.enemyInfo.enemyCanAttackPeriod)
        self.canAttackTimer.reset()


    def process(self, dt):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy) 

        self.lastInputTimer.advance(dt)
        self.canAttackTimer.advance(dt)

        # manage speed
        if self.lastInputTimer.timeIsUp():
            self.getInputChase()
            self.lastInputTimer.reset()
        
        if self.canAttackTimer.timeIsUp():
            if self.canAttackPlayer():
                if meEnemy.world.director.canHaveMoreEnemiesAttacking():
                    self.brain.pop()
                    self.brain.push("attackwindup")
                    self.canAttackTimer.reset()

        if self.timeIsUp():
            logger.debug("{}: Too long chasing, switching to wander".format(self.owner))
            self.brain.pop()
            self.brain.push("wander")


    def canAttackPlayer(self):
        for message in messaging.get(): 
            if message.type is MessageType.PlayerLocation:
                ret = self.checkHitLocation(message.data)
                if ret is True: 
                    return True
        
        return False


    def checkHitLocation(self, playerLocation): 
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy) 

        attackRendable = self.brain.owner.world.component_for_entity(
            meEnemy.offensiveAttackEntity, system.renderable.Renderable)
        hitLocations = attackRendable.texture.getTextureHitCoordinates()

        # only one of the hitlocations need to hit
        for hitLocation in hitLocations:
            canAttack = Utility.pointIn(
                hitLocation, 
                playerLocation)

            if canAttack: 
                logger.debug("Can attack, me {} in {}".format(
                    hitLocation, playerLocation
                ))
                return True

        return False


    def getInputChase(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy) 

        if not meEnemy.enemyMovement: 
            return

        meOffensiveWeaponRenderable = self.brain.owner.world.component_for_entity(
            meEnemy.offensiveAttackEntity, system.renderable.Renderable)
        meWeaponLocation = meOffensiveWeaponRenderable.getLocation()
        playerLocation = meEnemy.player.getLocation()

        moveX = 0
        moveY = 0
        dontChangeDirection = False

        if meWeaponLocation.x < playerLocation.x:
            moveX = 1
        elif meWeaponLocation.x >= playerLocation.x + meEnemy.player.texture.width:
            moveX = -1

        # check if its better to just walk backwards
        meWeaponLocationInverted = meOffensiveWeaponRenderable.getLocationDirectionInverted()
        distanceNormal = Utility.distance(playerLocation, meWeaponLocation)
        distanceInverted = Utility.distance(playerLocation, meWeaponLocationInverted)
        if distanceNormal['sum'] < distanceInverted['sum']:
            dontChangeDirection = True

        # we can walk diagonally, no elif here
        if meWeaponLocation.y < playerLocation.y:
            moveY = 1
        elif meWeaponLocation.y > playerLocation.y + meEnemy.player.texture.height - 1: # why -1?
            moveY = -1

        meRenderable.move(moveX, moveY, dontChangeDirection)