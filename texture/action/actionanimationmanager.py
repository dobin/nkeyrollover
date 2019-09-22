import logging

from common.direction import Direction
from texture.action.actiontype import ActionType
from utilities.utilities import Utility
from texture.animation import Animation
from texture.texturehelper import TextureHelper

logger = logging.getLogger("actionAnimationManager")


class ActionAnimationManager(object):
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}


    def loadFiles(self):
        self.animationsLeft = {}
        self.animationsRight = {}

        for actiontype in ActionType:
            self.animationsLeft[actiontype] = self.createAnimation(
                actiontype, Direction.left)
            logging.info("LOADL: {}".format(actiontype))

        for actiontype in ActionType:
            self.animationsRight[actiontype] = self.createAnimation(
                actiontype, Direction.right)
            logging.info("LOADR: {}".format(actiontype))


    def getAnimation(self, actionType, direction):
        if direction is Direction.left:
            return self.animationsLeft[actionType]
        else:
            return self.animationsRight[actionType]


    def createAnimation(self, actionType, direction):
        animation = self.readAction(actionType=actionType)
        if animation.originalDirection is not direction:
            Utility.mirrorFrames(animation.arr)

        Utility.checkAnimation(animation, actionType, None)

        return animation


    def readAction(self, actionType :ActionType) -> Animation:
        actionName = actionType.name
        filename = "data/textures/action/{}.ascii".format(actionName)
        animation = TextureHelper.readAnimationFile(filename)
        animation.name = actionName

        filenameYaml = "data/textures/action/{}.yaml".format(actionName)
        TextureHelper.loadYamlIntoAnimation(filenameYaml, animation)

        return animation
