import logging

logger = logging.getLogger(__name__)


class PassiveAttack(object):
    def __init__(self, attackFrames):
        self.attackFrames = attackFrames
