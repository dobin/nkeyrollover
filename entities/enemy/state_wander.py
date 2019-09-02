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
from directmessaging import directMessaging, DirectMessage, DirectMessageType


logger = logging.getLogger(__name__)


class StateWander(State):
    name = "wander"

    def __init__(self, brain):
        State.__init__(self, brain)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)
        self.lastInputTimer = Timer( meEnemy.enemyInfo.wanderStepDelay, instant=True )
        self.destCoord = Coordinates()
        self.destIsPoint = False


    def on_enter(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        stateTimeRnd = random.randrange(
            -100 * meEnemy.enemyInfo.wanderTimeRnd,
            100 * meEnemy.enemyInfo.wanderTimeRnd)
        self.setTimer( meEnemy.enemyInfo.wanderTime + (stateTimeRnd / 100) )
        self.chooseDestination()


    def process(self, dt):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)


        self.lastInputTimer.advance(dt)

        if self.lastInputTimer.timeIsUp():
            self.getInputWander()
            self.lastInputTimer.reset()

        if self.timeIsUp():
            if meEnemy.director.canHaveMoreEnemiesChasing():
                logger.debug("{}: Too long wandering, chase again a bit".format(self.owner))
                self.brain.pop()
                self.brain.push("chase")

        elif Utility.isIdentical(meRenderable.getLocation(), self.destCoord):
            # No reset of wander state atm, just a new location
            self.chooseDestination()

        else:
            # check if player is close
            for message in messaging.get():
                if message.type is MessageType.PlayerLocation:
                    distance = Utility.distance(
                        message.data,
                        meRenderable.getLocation())

                    if distance['sum'] < 10:
                        logger.info("{}: Player is close, chasing".format(self.owner))
                        self.brain.pop()
                        self.brain.push("chase")


    def getInputWander(self):
        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)
        meGroupId = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.groupid.GroupId)

        if not meRenderable.enemyMovement:
            return

        x = 0
        y = 0
        if self.destCoord.x > meRenderable.coordinates.x:
            x=1
        elif self.destCoord.x < meRenderable.coordinates.x:
            x=-1

        if self.destCoord.y > meRenderable.coordinates.y:
            y=1
        elif self.destCoord.y < meRenderable.coordinates.y:
            y=-1

        directMessaging.add(
            groupId = meGroupId.getId(),
            type = DirectMessageType.moveEnemy,
            data = {
                'x': x,
                'y': y,
                'dontChangeDirection': False,
            },
        )


    def chooseDestination(self):
        meEnemy = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.gamelogic.enemy.Enemy)

        meRenderable = self.brain.owner.world.component_for_entity(
            self.brain.owner.entity, system.renderable.Renderable)

        # if true:  go to a static point close to the current enemy position
        # if false: go to a point relative to the enemy
        #self.destIsPoint = random.choice([True, False])

        # note that getLocation() will return a reference. we need to copy it here.
        self.destCoord.x = meEnemy.player.getLocation().x
        self.destCoord.y = meEnemy.player.getLocation().y
        self.destCoord = self.pickDestAroundPlayer(self.destCoord, meRenderable)
        if meEnemy.world.showEnemyWanderDestination:
            meEnemy.world.textureEmiter.showCharAtPos(
                char='.', timeout=self.timer, coordinate=self.destCoord, color=Color.grey)


    def pickDestAroundPlayer(self, coord :Coordinates, meRenderable):
        ptRight = random.choice([True, False])
        ptDown = random.choice([True, False])

        if ptRight:
            coord.x += 6 + random.randint(0, 5)
        else:
            coord.x -= 6 + random.randint(0, 5)

        if ptDown:
            coord.y += 4 + random.randint(0, 5)
            if coord.y > Config.rows - 2 - meRenderable.texture.height:
                coord.y = Config.rows - 2 - meRenderable.texture.height
        else:
            coord.y -= 4 + random.randint(0, 5)
            # +1 so they can overlap only a bit on top
            if coord.y < Config.topborder - meRenderable.texture.height + 1:
                coord.y = Config.topborder  - meRenderable.texture.height + 1

        # make sure destination is on-screen
        if coord.x < Config.topborder:
            coord.x = Config.topborder
        if coord.x > Config.rows + meRenderable.texture.height:
            coord.x = Config.rows + meRenderable.texture.height

        return coord
