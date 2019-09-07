import logging

logger = logging.getLogger(__name__)


class Player():
    def __init__(self):
        self.name = 'Player'
        self.points = 0
        self.isPlayer = True

    def advance(self, deltaTime :float):
        pass

    def __repr__(self):
        return "Player"
