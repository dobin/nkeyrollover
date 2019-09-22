import logging

from common.direction import Direction
from texture.phenomena.phenomenatype import PhenomenaType
from utilities.utilities import Utility
from texture.animation import Animation
from texture.texturehelper import TextureHelper

logger = logging.getLogger("phenomenaAnimationManager")


class PhenomenaAnimationManager(object):
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}


    def loadFiles(self):
        self.animationsLeft = {}
        self.animationsRight = {}

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
        animation = self.readPhenomena(
            phenomenaType=phenomenaType)
        if animation.originalDirection is not direction:
            Utility.mirrorFrames(animation.arr)

        Utility.checkAnimation(animation, phenomenaType, None)

        return animation


    def readPhenomena(
        self,
        phenomenaType :PhenomenaType,
    ) -> Animation:
        phenomenaName = phenomenaType.name
        filename = "data/textures/phenomena/{}.ascii".format(phenomenaName)
        animation = TextureHelper.readAnimationFile(filename)
        animation.name = phenomenaName

        filenameYaml = "data/textures/phenomena/{}.yaml".format(phenomenaName)
        TextureHelper.loadYamlIntoAnimation(filenameYaml, animation)
        return animation
