import random


from ai.brain import Brain
from ai.states import BaseState as State
from texture.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer


import logging
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
        self.chaseTimer = Timer(0.5, instant=True)


    def on_enter(self):
        me = self.brain.owner
        self.setTimer( me.enemyInfo.chaseTime )
        self.chaseTimer.init()
        me.sprite.changeTexture(CharacterAnimationType.walking, me.direction)


    def process(self, dt):
        self.chaseTimer.advance(dt)

        if self.chaseTimer.timeIsUp(): 
            #logger.debug("I'm moving / chasing!")
            self.chaseTimer.reset()
        
        me = self.brain.owner
        me.getInputChase()  # TODO move here?

        if self.brain.owner.canReachPlayer():
            self.brain.pop()
            self.brain.push("attackwindup")

        if self.timeIsUp():
            logging.debug("{}: Too long chasing, switching to wander".format(self.owner))
            self.brain.pop()
            self.brain.push("wander")


class AttackWindup(State): 
    name = 'attackwindup'


    def on_enter(self):
        me = self.brain.owner
        me.sprite.changeTexture(CharacterAnimationType.hitwindup, me.direction)

        self.setTimer( self.brain.owner.enemyInfo.windupTime )


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
        self.wanderTimer = Timer(0.5, instant=True)


    def on_enter(self):
        me = self.brain.owner

        self.wanderTimer.init()
        me.sprite.changeTexture(CharacterAnimationType.walking, me.direction)
        self.setTimer( me.enemyInfo.wanderTime )


    def process(self, dt):
        self.wanderTimer.advance(dt)
        me = self.brain.owner

        if self.wanderTimer.timeIsUp(): 
            #logger.debug("I'm moving / wander!")
            self.wanderTimer.reset()
        
        me.getInputWander() # TODO move this here?

        if self.timeIsUp():
            logging.debug("{}: Too long wandering, chase again a bit".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")

        elif self.brain.owner.isPlayerClose():
            logging.debug("{}: Player is close, chasing".format(self.owner))
            self.brain.pop()
            self.brain.push("chase")



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


        self.setTimer( me.dyingTime )


    def process(self, dt):
        if self.timeIsUp():
            logging.debug("{}: Died enough, set to inactive".format(self.owner))
            self.brain.pop()
            self.brain.push("idle")
            self.brain.owner.setActive(False)




