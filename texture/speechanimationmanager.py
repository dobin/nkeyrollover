from entities.direction import Direction
from .animation import Animation


class SpeechAnimationManager(object):
    def __init__(self):
        pass

    def getAnimation(self, displayText=None, direction=Direction.right): 
        animation = Animation()

        animation.width = 5
        animation.height = 4
        animation.frameCount = 1
        animation.frameTime = [
            1.5,
        ]
        animation.endless = False
        animation.advanceByStep = False

        animation.arr = [
            [
                [ '.', '-', '-', '-', '.' ],
                [ '|', 'h', 'o', 'i', '|' ],
                [ '`', '^', '-', '-', '\'' ],
                [ '/', ' ', ' ', ' ', ' ' ],                        
            ]
        ]

        return animation
