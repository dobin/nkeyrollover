import logging
import collections

from utilities.timer import Timer
from utilities.utilities import Utility

logger = logging.getLogger(__name__)


class Attackable():
    def __init__(self, initialHealth=100, stunTime=0.75, stunCount=3, stunTimeFrame=3):
        self.health = initialHealth
        self.initialHealth = initialHealth

        self.maxStunCount = stunCount
        self.stunTimeFrame = stunTime * 1000
        self.stunTime = stunTime

        self.isStunned = False
        self.stunTimer = Timer(0.0)
        self.stunTimer.setActive(False)
        self.stunnedQueue = collections.deque(maxlen=5)


    def isStunnable(self):
        timeRef = Utility.getTimeMs() - self.stunTimeFrame
        stunCount = 0
        for stunned in self.stunnedQueue:
            if stunned['time'] > timeRef:
                stunCount += 1

        if stunCount < self.maxStunCount:
            logger.debug("Stun check: Can be stunned")
            return True
        else:
            logger.debug("Stun check: Can not be stunned")
            return False


    def addStun(self, stunTime):
        self.stunnedQueue.append({
            'time': Utility.getTimeMs(),
            'stunTime': stunTime
        })


    def resetHealth(self):
        self.health = self.initialHealth


    def adjustHealth(self, health :int):
        self.health += health
        logger.info("Got damage: {}  new health: {}".format(health, self.health))


    def getHealth(self):
        return self.health


    def advance(self, dt):
        self.stunTimer.advance(dt)
