import logging
from enum import Enum

from entities.characterstatus import CharacterStatus

logger = logging.getLogger(__name__)


class PlayerState(Enum):
    spawn = 0
    walking = 1

    dying = 2
    idle = 3

    attacking = 4
    attackskill = 5


class Player():
    def __init__(self):
        self.characterStatus = CharacterStatus()
        self.name = 'Player'
        self.points = 0
        self.state = PlayerState.spawn


    def advance(self, deltaTime :float):
        self.characterStatus.advance(deltaTime)


    def setState(self, state): 
        self.state = state


    def __repr__(self):
        return "Player"
