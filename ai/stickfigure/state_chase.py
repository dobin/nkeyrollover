import random
import logging

from stackfsm.states import BaseState as State
from utilities.timer import Timer

from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
import system.graphics.renderable
import system.gamelogic.enemy
from utilities.entityfinder import EntityFinder
from config import Config
from ai.aihelper import AiHelper

logger = logging.getLogger(__name__)


class StateChase(State):
    name = "chase"

    def __init__(self, brain):
        State.__init__(self, brain)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        # basically move speed
        self.lastInputTimer = Timer(
            meEnemy.enemyInfo.chaseStepDelay,
            instant=True)

        # try attacking when timer is finished
        self.canAttackTimer = Timer()

        # we need to know player location, or we could just handle on every new
        # PlayerLocation message
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

        if not Config.enemyAttacking:
            self.canAttackTimer.setActive(False)


    def tryAttacking(self):
        if self.canAttackTimer.timeIsUp():
            logger.debug("{}: Check if i can attack player".format(self.name))
            if self.canAttackPlayer():
                if (EntityFinder.numEnemiesInState(self.brain.owner.world, 'attack')
                        < Config.enemiesInStateAttacking):
                    self.brain.pop()
                    self.brain.push("attackwindup")

            self.canAttackTimer.reset()


    def tryMoving(self):
        # only move if we can not hit him (even on cooldown)
        # this is quiet... taxing. and not really necessary?
        # if not self.canAttackPlayer():

        if True:
            # movement speed, and direction
            if self.lastInputTimer.timeIsUp():
                self.getInputChase()
                self.lastInputTimer.reset()


    def trySkill(self):
        # stickfigure has no skills
        pass


    def process(self, dt):
        meAttackable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.attackable.Attackable)

        if meAttackable.isStunned:
            return

        self.lastInputTimer.advance(dt)
        self.canAttackTimer.advance(dt)

        # update player position if new location
        self.checkForNewPlayerPosition()

        self.tryAttacking()
        # note that if we want to attack, as identified a few lines above,
        # we will be in state attackWindup, and not reach here
        self.trySkill()
        self.tryMoving()

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
        if self.lastKnownPlayerPosition is None:
            # we may not yet have received a location.
            # find it directly via player entity
            # this is every time we go into chase state
            playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
            # player not spawned
            if playerEntity is not None:
                playerRenderable = self.brain.owner.world.component_for_entity(
                    playerEntity, system.graphics.renderable.Renderable)
                self.lastKnownPlayerPosition = playerRenderable.getLocationAndSize()

        canAttack = AiHelper.canAttackPlayer(
            self.brain.owner, self.lastKnownPlayerPosition)

        return canAttack


    def getInputChase(self):
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.graphics.renderable.Renderable)

        if not Config.enemyMovement:
            return

        moveX, moveY, dontChangeDirection = AiHelper.getAttackVectorToPlayer(
            self.owner, meRenderable)

        # only move if we really move a character
        if moveX != 0 or moveY != 0:
            directMessaging.add(
                groupId = meGroupId.getId(),
                type = DirectMessageType.moveEnemy,
                data = {
                    'x': moveX,
                    'y': moveY,
                    'dontChangeDirection': dontChangeDirection,
                    'updateTexture': True,
                    'force': False,
                },
            )
