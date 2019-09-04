import logging
from enum import Enum

from entities.characterstatus import CharacterStatus

logger = logging.getLogger(__name__)


class Player():
    def __init__(self):
        self.characterStatus = CharacterStatus()
        self.name = 'Player'
        self.points = 0

    def advance(self, deltaTime :float):
        self.characterStatus.advance(deltaTime)

    def __repr__(self):
        return "Player"
