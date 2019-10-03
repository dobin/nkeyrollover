import random
import logging

from stackfsm.states import BaseState as State
from utilities.timer import Timer
from config import Config
from common.coordinates import Coordinates
from utilities.utilities import Utility
from utilities.color import Color
from utilities.entityfinder import EntityFinder
import system.graphics.renderable
import system.gamelogic.enemy
from directmessaging import directMessaging, DirectMessageType
from messaging import messaging, MessageType
from ai.aihelper import AiHelper

logger = logging.getLogger(__name__)


class StateWander(State):
    name = "wander"

    def __init__(self, brain):
        State.__init__(self, brain)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)
        self.lastInputTimer = Timer(meEnemy.enemyInfo.wanderStepDelay, instant=True)
        self.destCoord = Coordinates()
        self.destIsPoint = False


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        stateTimeRnd = random.randrange(
            -100 * meEnemy.enemyInfo.wanderTimeRnd,
            100 * meEnemy.enemyInfo.wanderTimeRnd)
        self.setTimer(meEnemy.enemyInfo.wanderTime + (stateTimeRnd / 100))
        self.chooseDestination()


    def process(self, dt):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.graphics.renderable.Renderable)
        meAttackable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.attackable.Attackable)

        if meAttackable.isStunned:
            return

        self.lastInputTimer.advance(dt)

        if self.lastInputTimer.timeIsUp():
            self.getInputWander()
            self.lastInputTimer.reset()

        if self.timeIsUp():
            if (EntityFinder.numEnemiesInState(self.brain.owner.world, 'chase')
                    < Config.enemiesInStateChase):
                logger.info("{}: Too long wandering, chase again a bit".format(
                    self.owner))
                self.brain.pop()
                self.brain.push("chase")

        elif Utility.isIdentical(meRenderable.getLocation(), self.destCoord):
            # No reset of wander state atm, just a new location
            self.chooseDestination()

        else:
            # check if player is close
            for message in messaging.getByType(MessageType.PlayerLocation):
                distance = Utility.distance(
                    message.data,
                    meRenderable.getLocation())

                if distance['sum'] < 10:
                    logger.info("{}: Player is close, chasing".format(self.owner))
                    self.brain.pop()
                    self.brain.push("chase")


    def getInputWander(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.graphics.renderable.Renderable)
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)

        if not Config.enemyMovement:
            return

        x, y = AiHelper.getVectorToPlayer(
            source=meRenderable.coordinates, dest=self.destCoord)

        directMessaging.add(
            groupId = meGroupId.getId(),
            type = DirectMessageType.moveEnemy,
            data = {
                'x': x,
                'y': y,
                'dontChangeDirection': False,
                'updateTexture': True,
            },
        )


    def chooseDestination(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.graphics.renderable.Renderable)

        # if true:  go to a static point close to the current enemy position
        # if false: go to a point relative to the enemy
        # self.destIsPoint = random.choice([True, False])

        # note that getLocation() will return a reference. we need to copy it here.
        playerEntity = EntityFinder.findPlayer(self.brain.owner.world)
        if not playerEntity:
            return
        playerRenderable = self.brain.owner.world.component_for_entity(
            playerEntity, system.graphics.renderable.Renderable)
        self.destCoord.x = playerRenderable.getLocation().x
        self.destCoord.y = playerRenderable.getLocation().y
        self.destCoord = AiHelper.pickDestAroundPlayer(self.destCoord, meRenderable)
        if Config.showEnemyWanderDest:
            messaging.add(
                type=MessageType.EmitTextureMinimal,
                data={
                    'char': '.',
                    'timeout': self.timer,
                    'coordinate': self.destCoord,
                    'color': Color.grey
                }
            )
