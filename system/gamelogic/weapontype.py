from enum import Enum


class WeaponType(Enum):
    unittest = 0
    hit = 1
    hitSquare = 2
    hitLine = 3
    jumpKick = 4

    explosion = 5
    laser = 6
    cleave = 7

    heal = 8
    port = 9

    charge = 10  # for cow
    spitfire = 11  # for dragon
