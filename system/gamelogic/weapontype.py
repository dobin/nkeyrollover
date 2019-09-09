from enum import Enum


class WeaponType(Enum):
    default = 0
    hit = 1
    hitSquare = 2
    hitLine = 3
    jumpKick = 4

    explosion = 5
    laser = 6
    cleave = 7

    heal = 8
    port = 9
