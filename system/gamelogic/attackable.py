import logging
import collections

from utilities.timer import Timer
import system.singletons.gametime

logger = logging.getLogger(__name__)


class Attackable():
    def __init__(
        self, initialHealth=100, stunTime=0.75, stunCount=3, stunTimeFrame=3,
        knockdownChance=0.0, knockbackChance = 0.0
    ):
        self.health = initialHealth
        self.initialHealth = initialHealth

        self.knockdownChance = knockdownChance
        self.knockbackChance = knockbackChance

        self.maxStunCount = stunCount
        self.stunTimeFrame = stunTimeFrame
        self.stunTime = stunTime
        self.isStunned = False
        self.stunTimer = Timer(0.0)
        self.stunTimer.setActive(False)
        self.stunnedQueue = collections.deque(maxlen=5)

        # after message GameRestart, all Renderables are deleted - but not until
        # the next advance(). Upon restarting the map, if the user presses a key,
        # checkHeal() in AttackableProcessor would emit yet another stray
        # GameOver message. This is the fix.
        self.isActive = True


    def setActive(self, active):
        self.isActive = active


    def isStunnable(self):
        if self.maxStunCount == 0:
            return False

        timeRef = system.singletons.gametime.getGameTime() - self.stunTimeFrame
        stunCount = 0
        for stunned in self.stunnedQueue:
            if stunned['time'] > timeRef:
                stunCount += 1

        if stunCount <= self.maxStunCount:
            logging.info("Stun check: Can be stunned Cnt: {} max: {} time: {}".format(
                stunCount, self.maxStunCount, timeRef))
            return True
        else:
            logging.info("Stun check: Can not be stunned Cnt: {} max: {} time: {}".format(
                stunCount, self.maxStunCount, timeRef))
            return False


    def addStun(self, stunTime):
        self.stunnedQueue.append({
            'time': system.singletons.gametime.getGameTime(),
            'stunTime': stunTime
        })


    def resetHealth(self):
        self.health = self.initialHealth


    def adjustHealth(self, health :int):
        self.health += health


    def getHealth(self):
        return self.health


    def getHealthPercentage(self):
        p = self.health / self.initialHealth
        return p


    def advance(self, dt):
        self.stunTimer.advance(dt)


    def setHealth(self, health):
        self.health = health
        self.initialHealth = health


    def setStunTime(self, stunTime):
        self.stunTime = stunTime


    def setStunTimeFrame(self, stunTimeFrame):
        self.stunTimeFrame = stunTimeFrame


    def setMaxStunCount(self, maxStunCount):
        self.maxStunCount = maxStunCount


    def setKnockdownChance(self, knockdownChance):
        self.knockdownChance = knockdownChance


    def setKnockbackChance(self, knockbackChance):
        self.knockbackChance = knockbackChance
