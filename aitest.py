from ai.brain import Brain
import entities.enemy.aifsm as aifsm


import sys
import select 


class Agent:
    def __init__(self):
        self.brain = Brain(self)
        self.isActive = True

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

        self.playerClose = False


    def attack(self):
        print("I'm attacking!")

    def wander(self): 
        print("I'am wandering!")

    def chase(self): 
        print("I'am chasing")


    def kill(self): 
        a.brain.pop()
        a.brain.push("dying")
    
    def setActive(self, isActive): 
        self.isActive = isActive

    def isPlayerClose(self):
        return self.playerClose

    def update(self, dt):
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
        a.update(0.1)
        time.sleep(0.1)

        i = getInput()
        if i is not None: 
            if 'c' in i:
                a.playerClose = not a.playerClose
                print("Playerclose: " + str(a.playerClose))
            if 'k' in i:
                a.kill()