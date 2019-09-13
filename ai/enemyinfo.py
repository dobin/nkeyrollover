class EnemyInfo(object):
    def __init__(self):
        # static lenghts
        self.attackWindupTime = 1.0
        self.spawnTime = 1.0
        self.attackTime = 1.0  # should be synchronized with attack animation
        self.dyingTime = 1.0
        self.enemyCanAttackPeriod = 0.3

        # can have range
        self.wanderTime = 5.0
        self.wanderTimeRnd = 2.0
        self.chaseTime = 5.0
        self.chaseTimeRnd = 2.0

        # movement speed
        self.wanderStepDelay = 0.3
        self.chaseStepDelay = 0.2

        self.stunTime = 1.0
