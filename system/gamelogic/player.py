import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Player():
    def __init__(self):
        self.name = 'Player'
        self.points = 0

    def advance(self, deltaTime :float):
        pass

    def __repr__(self):
        return "Player"
