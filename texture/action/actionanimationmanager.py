import logging

from common.direction import Direction
from texture.action.actiontype import ActionType
from texture.filetextureloader import FileTextureLoader
from utilities.utilities import Utility

logger = logging.getLogger("actionAnimationManager")


class ActionAnimationManager(object):
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}
        self.fileTextureLoader = FileTextureLoader()

        for actiontype in ActionType:
            self.animationsLeft[actiontype] = self.createAnimation(
                actiontype, Direction.left)

        for actiontype in ActionType:
            self.animationsRight[actiontype] = self.createAnimation(
                actiontype, Direction.right)


    def getAnimation(self, actionType, direction):
        if direction is Direction.left:
            return self.animationsLeft[actionType]
        else:
            return self.animationsRight[actionType]


    def createAnimation(self, actionType, direction):
        animation = self.fileTextureLoader.readAction(
            actionType=actionType)
        if animation.originalDirection is not direction:
            Utility.mirrorFrames(animation.arr)

        Utility.checkAnimation(animation, actionType, None)

        return animation
