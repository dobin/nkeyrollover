class PlayerSeed(object):
    def __init__(self):
        self.initialHealth = 100
        self.stunCount = 2
        self.stunTimeFrame = 5.0

        self.stunTime = 0.75
        self.knockdownChance = 0.2
        self.knockbackChance = 0.2
