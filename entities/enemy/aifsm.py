import random
import logging

from ai.brain import Brain
from ai.states import BaseState as State
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from sprite.direction import Direction
from config import Config
from sprite.coordinates import Coordinates

logger = logging.getLogger(__name__)


class Idle(State):
    name = "idle"

    def __init__(self, brain):
        State.__init__(self, brain)

    def on_enter(self):
        pass

    def on_exit(self):
        pass


class Spawn(State):
    name = "spawn"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        me = self.brain.owner
        self.setTimer( me.enemyInfo.spawnTime )
        me.texture.changeAnimation(CharacterAnimationType.standing, me.direction)
        me.setActive(True)


    def process(self, dt):
        if self.timeIsUp():
            self.brain.pop()

            if Config.devMode: 
                # make him come straight at us, sucker
                self.brain.push("chase")
            else: 
                self.brain.push("wander")


class Chase(State):
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
        me.texture.changeAnimation(
            CharacterAnimationType.walking, 
            me.direction)


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
            if me.coordinates.x < Config.columns - me.texture.width - 1:
                me.coordinates.x += 1
                me.direction = Direction.right
        elif playerLocation.x < me.coordinates.x: 
            if me.coordinates.x > 1:
                me.coordinates.x -= 1
                me.direction = Direction.left

        if playerLocation.y > me.coordinates.y:
            if me.coordinates.y < Config.rows - me.texture.height - 1:
                me.coordinates.y += 1
        elif playerLocation.y < me.coordinates.y:
            if me.coordinates.y > 2:
                me.coordinates.y -= 1


class AttackWindup(State): 
    name = 'attackwindup'

    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.hitwindup, me.direction)

        self.setTimer( me.enemyInfo.windupTime )

    def process(self, dt):
        if self.timeIsUp():
            # windup animation done, lets do the attack
            self.brain.pop()
            self.brain.push("attack")


class Attack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.attackTimer = Timer() # Timer(0.5, instant=False) # windup and cooldown


    def on_enter(self):
        me = self.brain.owner
        self.attackTimer.init()
        me.texture.changeAnimation(CharacterAnimationType.hitting, me.direction)
        
        self.attackTimer.setTimer(me.texture.getAnimationTime())
        self.setTimer( me.texture.getAnimationTime() )

 
    def process(self, dt):
        self.attackTimer.advance(dt)
        me = self.brain.owner

        if self.attackTimer.timeIsUp(): 
            logger.warn(self.name + " I'm attacking!")
            self.attackTimer.reset()
            me.characterAttack.attack()

        if self.timeIsUp():
            # too long attacking. lets switch to chasing
            logger.debug("{}: Too long attacking, switch to chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")


class Wander(State):
    name = "wander"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.lastInputTimer = Timer( self.brain.owner.enemyInfo.wanderStepDelay, instant=True )
        self.destCoords = Coordinates()
        self.destIsPoint = False


    def on_enter(self):
        me = self.brain.owner
        me.texture.changeAnimation(CharacterAnimationType.walking, me.direction)
        stateTimeRnd = random.randrange(-100 * me.enemyInfo.wanderTimeRnd, 100 * me.enemyInfo.wanderTimeRnd)
        self.setTimer( me.enemyInfo.wanderTime + (stateTimeRnd / 100) )        

        # if true:  go to a static point close to the current enemy position
        # if false: go to a point relative to the enemy
        self.destIsPoint = random.choice([True, False])
        self.destCoord = self.pickDestAroundPlayer( me.player.getLocation() )


    def pickDestAroundPlayer(self, coord :Coordinates):
        ptRight = random.choice([True, False])
        ptDown = random.choice([True, False])

        if ptRight: 
            coord.x += 6
        else: 
            coord.x -= 6

        if ptDown: 
            coord.y += 4
        else: 
            coord.y -= 4

        return coord


    def process(self, dt):
        me = self.brain.owner
        self.lastInputTimer.advance(dt)

        if self.lastInputTimer.timeIsUp(): 
            self.getInputWander()
            self.lastInputTimer.reset()

        if self.timeIsUp():
            logger.debug("{}: Too long wandering, chase again a bit".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")

        elif me.isPlayerClose():
            logger.debug("{}: Player is close, chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")


    def getInputWander(self):
        me = self.brain.owner

        # make run-animation 
        me.texture.advanceStep()

        if not me.enemyMovement: 
            return

        if not self.destIsPoint:
            pass
            # TODO

        playerLocation = self.destCoord       
        if playerLocation.x > me.coordinates.x:
            if me.coordinates.x < Config.columns - me.texture.width - 1:
                me.coordinates.x += 1
                me.direction = Direction.right
        else: 
            if me.coordinates.x > 1:
                me.coordinates.x -= 1
                self.direction = Direction.left

        if playerLocation.y > me.coordinates.y:
            if me.coordinates.y < Config.rows - me.texture.height - 1:
                me.coordinates.y += 1
        else: 
            if me.coordinates.y > 2:
                me.coordinates.y -= 1


class Dying(State):
    name = "dying"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        me = self.brain.owner

        if random.choice([True, False]): 
            logger.info(self.name + " Death animation deluxe")
            animationIndex = random.randint(0, 1)
            me.world.makeExplode(me.texture, me.direction, None)
            me.texture.changeAnimation(CharacterAnimationType.dying, me.direction, animationIndex)
            me.setActive(False)
        else: 
            animationIndex = random.randint(0, 1)
            me.texture.changeAnimation(CharacterAnimationType.dying, me.direction, animationIndex)


        self.setTimer( me.enemyInfo.dyingTime )


    def process(self, dt):
        me = self.brain.owner

        if self.timeIsUp():
            logger.debug("{}: Died enough, set to inactive".format(self.owner))
            self.brain.pop()
            self.brain.push("idle")
            me.setActive(False)




