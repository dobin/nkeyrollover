from enum import Enum

class Action(Enum): 
    standing = 0
    walking = 1
    hitting = 2
    shrugging = 3
    hit = 4
    speech = 5
    dying = 6

    # for SpeckSprite
    flying = 7

    spawning = 10

    roflcopter = 20