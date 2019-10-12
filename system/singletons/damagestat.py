import logging

from utilities.timer import Timer

logger = logging.getLogger(__name__)


class DamageStat(object):
    def __init__(self):
        self.damage = 100
        self.dmgTimer = Timer(1.0)


    def addDamage(self, damage):
        self.damage += damage


    def process(self, dt):
        self.dmgTimer.advance(dt)
        if self.dmgTimer.timeIsUp():
            self.dmg -= 10
            self.dmgTimer.reset()


    def getDamageStat(self):
        return self.damage


damageStat = DamageStat()
