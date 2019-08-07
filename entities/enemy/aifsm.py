import random
import logging

from ai.brain import Brain
from ai.states import BaseState as State
from texture.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from entities.direction import Direction
from config import Config

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
        me.sprite.changeTexture(CharacterAnimationType.standing, me.direction)
        me.setActive(True)


    def process(self, dt):
        if self.timeIsUp():
            self.brain.pop()
            self.brain.push("chase")


class Chase(State):
    name = "chase"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.lastInputTimer = Timer( self.brain.owner.enemyInfo.chaseStepDelay, instant=True )

    def on_enter(self):
        me = self.brain.owner
        self.setTimer( me.enemyInfo.chaseTime )
        me.sprite.changeTexture(CharacterAnimationType.walking, me.direction)


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
            logging.debug("{}: Too long chasing, switching to wander".format(self.owner))
            self.brain.pop()
            self.brain.push("wander")


    def getInputChase(self):
        me = self.brain.owner

        # make run-animation 
        me.sprite.advanceStep()

        playerLocation = me.player.getLocation()

        if playerLocation['x'] > me.x:
            if me.x < Config.columns - me.sprite.texture.width - 1:
                me.x += 1
                me.direction = Direction.right
        else: 
            if me.x > 1:
                me.x -= 1
                me.direction = Direction.left

        if playerLocation['y'] > me.y:
            if me.y < Config.rows - me.sprite.texture.height - 1:
                me.y += 1
        else: 
            if me.y > 2:
                me.y -= 1


class AttackWindup(State): 
    name = 'attackwindup'

    def on_enter(self):
        me = self.brain.owner
        me.sprite.changeTexture(CharacterAnimationType.hitwindup, me.direction)

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
        self.attackTimer = Timer(0.5, instant=False) # windup and cooldown


    def on_enter(self):
        me = self.brain.owner
        self.attackTimer.init()
        me.sprite.changeTexture(CharacterAnimationType.hitting, me.direction)
        self.setTimer( me.enemyInfo.attackTime )


    def process(self, dt):
        self.attackTimer.advance(dt)
        me = self.brain.owner

        if self.attackTimer.timeIsUp(): 
            logger.warn(self.name + " I'm attacking!")
            self.attackTimer.reset()
            me.characterAttack.attack()

        if self.timeIsUp():
            # too long attacking. lets switch to chasing
            logging.debug("{}: Too long attacking, switch to chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")


class Wander(State):
    name = "wander"

    def __init__(self, brain):
        State.__init__(self, brain)
        self.lastInputTimer = Timer( self.brain.owner.enemyInfo.wanderStepDelay, instant=True )


    def on_enter(self):
        me = self.brain.owner
        me.sprite.changeTexture(CharacterAnimationType.walking, me.direction)
        self.setTimer( me.enemyInfo.wanderTime )


    def process(self, dt):
        me = self.brain.owner
        self.lastInputTimer.advance(dt)

        if self.lastInputTimer.timeIsUp(): 
            self.getInputWander()
            self.lastInputTimer.reset()

        if self.timeIsUp():
            logging.debug("{}: Too long wandering, chase again a bit".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")

        elif me.isPlayerClose():
            logging.debug("{}: Player is close, chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")


    def getInputWander(self):
        me = self.brain.owner

        # make run-animation 
        me.sprite.advanceStep()

        playerLocation = me.player.getLocation()

        if playerLocation['y'] > me.y:
            # newdest is higher
            playerLocation['y'] -= 6
            
            if playerLocation['x'] > me.x:
                playerLocation['x'] += 9
            else:
                playerLocation['x'] -= 9

        else: 
            # newdest is lower
            playerLocation['y'] += 6
            
            if playerLocation['x'] > me.x:
                playerLocation['x'] += 9
            else:
                playerLocation['x'] -= 9


        if playerLocation['x'] > me.x:
            if me.x < Config.columns - me.sprite.texture.width - 1:
                me.x += 1
                me.direction = Direction.right
        else: 
            if me.x > 1:
                me.x -= 1
                self.direction = Direction.left

        if playerLocation['y'] > me.y:
            if me.y < Config.rows - me.sprite.texture.height - 1:
                me.y += 1
        else: 
            if me.y > 2:
                me.y -= 1


class Dying(State):
    name = "dying"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        me = self.brain.owner

        if random.choice([True, False]): 
            logger.info(self.name + " Death animation deluxe")
            animationIndex = random.randint(0, 1)
            me.world.makeExplode(me.sprite, me.direction, None)
            me.sprite.changeTexture(CharacterAnimationType.dying, me.direction, animationIndex)
            me.setActive(False)
        else: 
            animationIndex = random.randint(0, 1)
            me.sprite.changeTexture(CharacterAnimationType.dying, me.direction, animationIndex)


        self.setTimer( me.enemyInfo.dyingTime )


    def process(self, dt):
        me = self.brain.owner

        if self.timeIsUp():
            logging.debug("{}: Died enough, set to inactive".format(self.owner))
            self.brain.pop()
            self.brain.push("idle")
            me.setActive(False)




