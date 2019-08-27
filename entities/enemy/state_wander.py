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



class StateWander(State):
    name = "wander"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.lastInputTimer = Timer( self.brain.owner.enemyInfo.wanderStepDelay, instant=True )
        self.destCoord = Coordinates()
        self.destIsPoint = False


    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.walking, me.direction)
        stateTimeRnd = random.randrange(
            -100 * me.enemyInfo.wanderTimeRnd, 
            100 * me.enemyInfo.wanderTimeRnd)
        self.setTimer( me.enemyInfo.wanderTime + (stateTimeRnd / 100) )
        self.chooseDestination()


    def process(self, dt):
        me = self.brain.owner
        self.lastInputTimer.advance(dt)

        if self.lastInputTimer.timeIsUp(): 
            self.getInputWander()
            self.lastInputTimer.reset()

        if self.timeIsUp():
            if me.world.director.canHaveMoreEnemiesChasing():
                logger.debug("{}: Too long wandering, chase again a bit".format(self.owner))
                self.brain.pop()
                self.brain.push("chase")

        elif me.isPlayerClose():
            logger.debug("{}: Player is close, chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")

        elif Utility.isIdentical(me.getLocation(), self.destCoord):
            # No reset of wander state atm, just a new location
            self.chooseDestination()


    def getInputWander(self):
        me = self.brain.owner

        # make run-animation 
        me.texture.advanceStep()

        if not me.enemyMovement: 
            return

        if self.destCoord.x > me.coordinates.x:
            me.move(x=1, y=0)
        elif self.destCoord.x < me.coordinates.x: 
            me.move(x=-1, y=0)

        if self.destCoord.y > me.coordinates.y:
            me.move(x=0, y=1)
        elif self.destCoord.y < me.coordinates.y: 
            me.move(x=0, y=-1)


    def chooseDestination(self): 
        me = self.brain.owner
        # if true:  go to a static point close to the current enemy position
        # if false: go to a point relative to the enemy
        #self.destIsPoint = random.choice([True, False])

        # note that getLocation() will return a reference. we need to copy it here.
        self.destCoord.x = me.player.getLocation().x
        self.destCoord.y = me.player.getLocation().y
        self.destCoord = self.pickDestAroundPlayer(self.destCoord, me)
        if me.world.showEnemyWanderDestination:
            me.world.textureEmiter.showCharAtPos(
                char='.', timeout=self.timer, coordinate=self.destCoord, color=Color.grey)


    def pickDestAroundPlayer(self, coord :Coordinates, me):
        ptRight = random.choice([True, False])
        ptDown = random.choice([True, False])

        if ptRight: 
            coord.x += 6 + random.randint(0, 5)
        else: 
            coord.x -= 6 + random.randint(0, 5)

        if ptDown: 
            coord.y += 4 + random.randint(0, 5)
            if coord.y > Config.rows - 2 - me.texture.height:
                coord.y = Config.rows - 2 - me.texture.height
        else: 
            coord.y -= 4 + random.randint(0, 5)
            # +1 so they can overlap only a bit on top
            if coord.y < Config.topborder - me.texture.height + 1:
                coord.y = Config.topborder  - me.texture.height + 1

        # make sure destination is on-screen
        if coord.x < Config.topborder: 
            coord.x = Config.topborder
        if coord.x > Config.rows + me.texture.height: 
            coord.x = Config.rows + me.texture.height

        return coord
