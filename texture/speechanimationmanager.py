from sprite.direction import Direction
from texture.animation import Animation


class SpeechAnimationManager(object):
    def __init__(self):
        pass

    def getAnimation(self, displayText=None, direction=Direction.right): 
        animation = Animation()

        animation.width = len(displayText) + 2
        animation.height = 4
        animation.frameCount = 1
        animation.frameTime = [
            1.5,
        ]
        animation.endless = False
        animation.advanceByStep = False

        l = animation.width

        animation.arr = [[]]
        l1 = []
        l1.append('.')
        l1.extend(list('-' * (l - 2)))
        l1.append('.')
        animation.arr[0].append(l1)

        l2 = []
        l2.append('|')
        l2.extend(list(displayText))
        l2.append('|')
        animation.arr[0].append(l2)

        l3 = []
        l3.append('`')
        l3.append(',')
        l3.extend(list('-' * (l - 3)))
        l3.append('\'')
        animation.arr[0].append(l3)

        l4 = []
        l4.append('/')
        l4.extend(list(' ' * (l - 1)))
        animation.arr[0].append(l4)

        #        [ '.', list('-' * (l - 2)), '.' ],
        #        [ '|', 'h', 'o', 'i', '|' ],
        #        [ '`', '^', list('-' * (l - 3)), '\'' ],
       #         [ '/', list('-' * (l - 1)), ],                        
        #    ]
        #]

        return animation
