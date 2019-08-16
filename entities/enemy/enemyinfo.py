from config import Config

class EnemyInfo(object): 
    def __init__(self): 
        # static lenghts
        self.windupTime = 0.5
        self.spawnTime = 1.0
        self.attackTime = 1.0
        self.dyingTime = 2.0
        self.enemyCanAttackPeriod = 0.3

        # can have range
        self.wanderTime = 5.0
        self.wanderTimeRnd = 2.0
        self.chaseTime = 5.0
        self.chaseTimeRnd = 2.0

        # movement speed
        self.wanderStepDelay = 0.5
        self.chaseStepDelay = 0.5

        if Config.devMode:
            self.wanderTime = 0.5
            self.spawnTime = 0.2
            self.chaseTime = 10.0