import logging

from common.direction import Direction
from texture.phenomena.phenomenatype import PhenomenaType
from texture.filetextureloader import FileTextureLoader
from utilities.utilities import Utility

logger = logging.getLogger("phenomenaAnimationManager")


class PhenomenaAnimationManager(object):
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}
        self.fileTextureLoader = FileTextureLoader()

        for phenomenatype in PhenomenaType:
            self.animationsLeft[phenomenatype] = self.createAnimation(
                phenomenatype, Direction.left)

        for phenomenatype in PhenomenaType:
            self.animationsRight[phenomenatype] = self.createAnimation(
                phenomenatype, Direction.right)


    def getAnimation(self, phenomenaType, direction):
        if direction is Direction.left:
            return self.animationsLeft[phenomenaType]
        else:
            return self.animationsRight[phenomenaType]


    def createAnimation(self, phenomenaType, direction):
        animation = self.fileTextureLoader.readPhenomena(
            phenomenaType=phenomenaType)
        if animation.originalDirection is not direction:
            Utility.mirrorFrames(animation.arr)

        Utility.checkAnimation(animation, phenomenaType, None)

        return animation
