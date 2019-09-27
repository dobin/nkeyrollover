from ai.enemyinfo import EnemyInfo


class EnemySeed(object):
    def __init__(self):
        self.characterTextureType = None
        self.weaponType = None
        self.health = None
        self.stunTime = None
        self.stunCount = None
        self.stunTimeFrame = None
        self.attackBaseLocation = None
        self.enemyInfo = EnemyInfo()
