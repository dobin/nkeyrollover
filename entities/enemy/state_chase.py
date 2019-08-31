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
from system.renderable import Renderable
from system.renderable import Renderable
import system.gamelogic.tenemy

logger = logging.getLogger(__name__)


class StateChase(State):
    name = "chase"

    def __init__(self, brain):
        State.__init__(self, brain)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.tenemy.tEnemy) 

        self.lastInputTimer = Timer( 
            meEnemy.enemyInfo.chaseStepDelay, 
            instant=True )
        self.canAttackTimer = Timer()


    def on_enter(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, Renderable)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.tenemy.tEnemy) 

        stateTimeRnd = random.randrange(-100 * meEnemy.enemyInfo.chaseTimeRnd, 100 * meEnemy.enemyInfo.chaseTimeRnd)
        self.setTimer( meEnemy.enemyInfo.chaseTime + (stateTimeRnd / 100) )
        meRenderable.texture.changeAnimation(
            CharacterAnimationType.walking, 
            meRenderable.direction)
        self.canAttackTimer.setTimer(meEnemy.enemyInfo.enemyCanAttackPeriod)
        self.canAttackTimer.reset()


    def process(self, dt):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.tenemy.tEnemy) 

        self.lastInputTimer.advance(dt)
        self.canAttackTimer.advance(dt)

        # manage speed
        if self.lastInputTimer.timeIsUp():
            self.getInputChase()
            self.lastInputTimer.reset()
        
        if self.canAttackTimer.timeIsUp():
            logger.info("Check if i can hit him...")
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
            self.brain.owner.entity, system.gamelogic.tenemy.tEnemy) 

        attackRendable = self.brain.owner.world.component_for_entity(
            meEnemy.offensiveAttackEntity, Renderable)
        hitLocations = attackRendable.texture.getTextureHitCoordinates()

        # only one of the hitlocations need to hit
        for hitLocation in hitLocations:
            canAttack = Utility.pointIn(
                hitLocation, 
                playerLocation)

            if canAttack: 
                logger.info("Can attack, me {} in {}".format(
                    hitLocation, playerLocation
                ))
                return True
            else: 
                logger.info("Can not attack, me {} in {}".format(
                    hitLocation, playerLocation
                ))

        return False


    def getInputChase(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, Renderable)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.tenemy.tEnemy) 

        # make run-animation 
        meRenderable.texture.advanceStep()

        if not meEnemy.enemyMovement: 
            return

        meOffensiveWeaponRenderable = self.brain.owner.world.component_for_entity(
            meEnemy.offensiveAttackEntity, Renderable)
        meWeaponLocation = meOffensiveWeaponRenderable.getLocation()
        logger.info("Enemy: {}  Weapon: {}".format(
            meRenderable.getLocation(), meWeaponLocation))
        playerLocation = meEnemy.player.getLocation()
        
        if meWeaponLocation.x < playerLocation.x:
            if meRenderable.coordinates.x < (meEnemy.viewport.getx() + Config.columns - meRenderable.texture.width - 1):
                meRenderable.coordinates.x += 1
                
                if meRenderable.direction is not Direction.right:
                    meRenderable.direction = Direction.right
                    meRenderable.texture.changeAnimation(
                        CharacterAnimationType.walking, 
                        meRenderable.direction)

        elif meWeaponLocation.x >= playerLocation.x + meEnemy.player.texture.width:
            if meRenderable.coordinates.x > 1 + meEnemy.viewport.getx():
                meRenderable.coordinates.x -= 1

                if meRenderable.direction is not Direction.left:
                    meRenderable.direction = Direction.left
                    meRenderable.texture.changeAnimation(
                        CharacterAnimationType.walking, 
                        meRenderable.direction)                

        # we can walk diagonally, no elif here

        if meWeaponLocation.y < playerLocation.y:
            if meRenderable.coordinates.y < Config.rows - meRenderable.texture.height - 1:
                meRenderable.coordinates.y += 1
        elif meWeaponLocation.y > playerLocation.y + meEnemy.player.texture.height - 1: # why -1?
            if meRenderable.coordinates.y > 2:
                meRenderable.coordinates.y -= 1