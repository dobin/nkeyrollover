import logging

from utilities.timer import Timer

logger = logging.getLogger(__name__)


class Player():
    def __init__(self):
        self.name = 'Player'
        self.points = 0
        self.isPlayer = True
        self.isAttacking = False
        self.isAlive = True

        self.attackTimer = Timer(0.0)


    def advance(self, deltaTime :float):
        self.attackTimer.advance(deltaTime)

        if self.attackTimer.timeIsUp():
            self.isAttacking = False
            self.attackTimer.setActive(False)


    def setAttacking(self, attackTime :float):
        self.isAttacking = True

        self.attackTimer.setTimer(attackTime)
        self.attackTimer.start()


    def setAlive(self, alive):
        self.isAlive = alive


    def __repr__(self):
        return "Player"
