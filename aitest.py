from ai.brain import Brain
import entities.enemy.aifsm as aifsm
from utilities.timer import Timer

import sys
import select 


class Agent:
    def __init__(self):
        self.active = True
        self.playerClose = False

        ###
        self.brain = Brain(self)
        
        self.stateData = {
            'spawn': {
                'state_time': 1.5,
            },
            'chase': {
                'state_time': 1.5,
            }, 
            'attack': {
                'state_time': 2.0,
            },
            'wander': {
                'state_time': 1.5,
            },
            'dying': {
                'state_time': 3.0,
            },
        }

        self.attackTimer = Timer(0.5, instant=True)
        self.wanderTimer = Timer(0.5, instant=True)
        self.chaseTimer = Timer(0.5, instant=True)


    # called by FSM
    def sAttackInit(self):
        self.attackTimer.init()

    def sAttack(self):
    	if self.attackTimer.timeIsUp(): 
            print("I'm attacking!")
            self.attackTimer.reset()


    def sWanderInit(self):
        self.wanderTimer.init()

    def sWander(self): 
        if self.wanderTimer.timeIsUp(): 
            print("I'm moving / wander!")
            self.wanderTimer.reset()


    def sChaseInit(self):
        self.chaseTimer.init()

    def sChase(self): 
        if self.chaseTimer.timeIsUp(): 
            print("I'm moving / chasing!")
            self.chaseTimer.reset()


    # Game Mechanics
    def gmKill(self): 
        self.brain.pop()
        self.brain.push("dying")


    # Other
    def setActive(self, active): 
        self.active = active

    def isPlayerClose(self):
        return self.playerClose

    def advance(self, dt):
        self.attackTimer.advance(dt)
        self.wanderTimer.advance(dt)
        self.chaseTimer.advance(dt)
        self.brain.update(dt)

    def __repr__(self):
        return '0x01'



def getInput(): 
    line = None
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline()
    
    return line


if __name__ == "__main__":
    import time
    a = Agent()
    a.brain.register(aifsm.Idle)
    a.brain.register(aifsm.Spawn)
    a.brain.register(aifsm.Attack)
    a.brain.register(aifsm.Chase)
    a.brain.register(aifsm.Wander)
    a.brain.register(aifsm.Dying)
    a.brain.push("spawn")
    
    while True:
        a.advance(0.1)
        time.sleep(0.1)

        i = getInput()
        if i is not None: 
            if 'c' in i:
                a.playerClose = not a.playerClose
                print("Playerclose: " + str(a.playerClose))
            if 'k' in i:
                a.gmKill()