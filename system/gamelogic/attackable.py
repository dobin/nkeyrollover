import logging
import collections

from utilities.timer import Timer
import system.singletons.gametime

logger = logging.getLogger(__name__)


class Attackable():
    def __init__(self, initialHealth=100, stunTime=0.75, stunCount=3, stunTimeFrame=3):
        self.health = initialHealth
        self.initialHealth = initialHealth

        self.maxStunCount = stunCount
        self.stunTimeFrame = stunTimeFrame
        self.stunTime = stunTime

        self.isStunned = False
        self.stunTimer = Timer(0.0)
        self.stunTimer.setActive(False)
        self.stunnedQueue = collections.deque(maxlen=5)


    def isStunnable(self):
        timeRef = system.singletons.gametime.getGameTime() - self.stunTimeFrame
        stunCount = 0
        for stunned in self.stunnedQueue:
            if stunned['time'] > timeRef:
                stunCount += 1

        if stunCount <= self.maxStunCount:
            logger.info("Stun check: Can be stunned {} {} {}".format(stunCount, timeRef, self.maxStunCount))
            return True
        else:
            logger.info("Stun check: Can not be stunned {} {}".format(stunCount, timeRef))
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
        logger.info("Got damage: {}  new health: {}".format(health, self.health))


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
