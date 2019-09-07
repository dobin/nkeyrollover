import logging

from texture.phenomena.phenomenaanimationmanager import PhenomenaAnimationManager
from texture.animationtexture import AnimationTexture
from sprite.coordinates import Coordinates

logger = logging.getLogger(__name__)


class PhenomenaTexture(AnimationTexture):
    def __init__(self, phenomenaType=None, direction=None):
        super(PhenomenaTexture, self).__init__()
        self.phenomenaAnimationManager = PhenomenaAnimationManager()

        if phenomenaType is not None:
            self.changeAnimation(phenomenaType, direction)


    def changeAnimation(self, phenomenaType, direction):
        self.animation = self.phenomenaAnimationManager.getAnimation(
            phenomenaType,
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
