

class EnemyInfo(object): 
    def __init__(self): 
        self.windupTime = 0.2

        self.spawnTime = 1.0
        self.wanderTime = 1.0 # 5.0
        self.chaseTime = 3.0 # 5.0
        self.attackTime = 2.0
        self.dyingTime = 2.0

        self.wanderStepDelay = 0.5
        self.chaseStepDelay = 0.5