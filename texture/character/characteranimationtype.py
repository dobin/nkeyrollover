from enum import Enum


class CharacterAnimationType(Enum):
    standing = 0
    walking = 1
    hitting = 2
    shrugging = 3
    dying = 4
    hitwindup = 5
    stun = 6

    hitWhip = 7
    knockdown = 8
    onhit = 9
    holdshield = 10
