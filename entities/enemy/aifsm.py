from ai.brain import Brain
from ai.states import BaseState as State


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
        self.setTimer( self.brain.owner.stateData[self.name]['state_time'])


    def process(self, dt):
        if self.timeIsUp():
            self.brain.pop()
            self.brain.push("chase")


class Chase(State):
    name = "chase"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        self.setTimer( self.brain.owner.stateData[self.name]['state_time'])


    def process(self, dt):
        if self.brain.owner.isPlayerClose():
            self.brain.pop()
            self.brain.push("attack")            

        if self.timeIsUp():
            print("Too long chasing, switching to wander")
            self.brain.pop()
            self.brain.push("wander")


class Attack(State):
    name = "attack"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        self.setTimer( self.brain.owner.stateData[self.name]['state_time'])


    def process(self, dt):
        self.brain.owner.attack()

        if self.timeIsUp():
            # too long attacking. lets switch to chasing
            print("Too long attacking, switch to chasing")
            self.brain.pop()
            self.brain.push("chase")


class Wander(State):
    name = "wander"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        self.setTimer( self.brain.owner.stateData[self.name]['state_time'])


    def process(self, dt):
        if self.timeIsUp():
            print("Too long wandering, chase again a bit")
            self.brain.pop()
            self.brain.push("chase")


class Dying(State):
    name = "dying"

    def __init__(self, brain):
        State.__init__(self, brain)


    def on_enter(self):
        self.setTimer( self.brain.owner.stateData[self.name]['state_time'])


    def process(self, dt):
        if self.timeIsUp():
            print("Died enough, set to inactive")
            self.brain.pop()
            self.brain.push("idle")
            self.brain.owner.setActive(False)




