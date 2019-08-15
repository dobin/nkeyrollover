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

logger = logging.getLogger(__name__)


class StateChase(State):
    name = "chase"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.lastInputTimer = Timer( 
            self.brain.owner.enemyInfo.chaseStepDelay, 
            instant=True )


    def on_enter(self):
        me = self.brain.owner
        stateTimeRnd = random.randrange(-100 * me.enemyInfo.chaseTimeRnd, 100 * me.enemyInfo.chaseTimeRnd)
        self.setTimer( me.enemyInfo.chaseTime + (stateTimeRnd / 100) )
        me.texture.changeAnimation(CharacterAnimationType.walking, me.direction)


    def process(self, dt):
        me = self.brain.owner
        self.lastInputTimer.advance(dt)

        # manage speed
        if self.lastInputTimer.timeIsUp():
            self.getInputChase()
            self.lastInputTimer.reset()
        
        if me.canReachPlayer():
            self.brain.pop()
            self.brain.push("attackwindup")

        if self.timeIsUp():
            logger.debug("{}: Too long chasing, switching to wander".format(self.owner))
            self.brain.pop()
            self.brain.push("wander")


    def getInputChase(self):
        me = self.brain.owner

        # make run-animation 
        me.texture.advanceStep()

        if not me.enemyMovement: 
            return

        playerLocation = me.player.getLocation()
        
        if playerLocation.x > me.coordinates.x:
            if me.coordinates.x < (me.viewport.getx() + Config.columns - me.texture.width - 1):
                me.coordinates.x += 1
                
                if me.direction is not Direction.right:
                    me.direction = Direction.right
                    me.texture.changeAnimation(
                        CharacterAnimationType.walking, me.direction)

        elif playerLocation.x < me.coordinates.x: 
            if me.coordinates.x > 1 + me.viewport.getx():
                me.coordinates.x -= 1

                if me.direction is not Direction.left:
                    me.direction = Direction.left
                    me.texture.changeAnimation(
                        CharacterAnimationType.walking, me.direction)                

        # we can walk diagonally 
        if playerLocation.y > me.coordinates.y:
            if me.coordinates.y < Config.rows - me.texture.height - 1:
                me.coordinates.y += 1
        elif playerLocation.y < me.coordinates.y:
            if me.coordinates.y > 2:
                me.coordinates.y -= 1