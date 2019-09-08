import logging

from texture.action.actionanimationmanager import ActionAnimationManager
from texture.animationtexture import AnimationTexture
from common.coordinates import Coordinates

logger = logging.getLogger(__name__)


class ActionTexture(AnimationTexture):
    def __init__(self, actionType=None, direction=None):
        super(ActionTexture, self).__init__()
        self.actionAnimationManager = ActionAnimationManager()

        if actionType is not None:
            self.changeAnimation(actionType, direction)


    def changeAnimation(self, actionType, direction):
        self.animation = self.actionAnimationManager.getAnimation(
            actionType,
            direction)
        self.init()
        self.width = self.animation.width
        self.height = self.animation.height


    def getTextureHitCoordinates(self, animationIdx=0):
        """For OffensiveAttack animation, get x/y which got hit"""
        locations = []

        x = 0
        while x < self.width:
            y = 0
            while y < self.height:
                if self.animation.arr[0][y][x] != '':
                    loc = Coordinates(x, y)
                    locations.append(loc)

                y += 1

            x += 1

        return locations
