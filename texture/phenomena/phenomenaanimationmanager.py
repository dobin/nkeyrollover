import logging

from sprite.direction import Direction
from texture.phenomena.phenomenatype import PhenomenaType
from texture.animation import Animation
from texture.filetextureloader import FileTextureLoader
from utilities.color import Color
from utilities.colorpalette import ColorPalette
from utilities.utilities import Utility

logger = logging.getLogger("phenomentaanimationmanager")


class PhenomenaAnimationManager(object):
    def __init__(self):
        self.animationsLeft = {}
        self.animationsRight = {}
        self.fileTextureLoader = FileTextureLoader()

        for phenomenatype in PhenomenaType:
            self.animationsLeft[phenomenatype] = self.createAnimation(phenomenatype, Direction.left)

        for phenomenatype in PhenomenaType:
            self.animationsRight[phenomenatype] = self.createAnimation(phenomenatype, Direction.right)


    def getAnimation(self, phenomenaType, direction):
        if direction is Direction.left:
            return self.animationsLeft[phenomenaType]
        else:
            return self.animationsRight[phenomenaType]


    def createAnimation(self, phenomenaType, direction):
        mapColor = ColorPalette.getColorByColor(Color.grey)
        weaponColor = ColorPalette.getColorByColor(Color.brightyellow)

        if phenomenaType is PhenomenaType.hit:
            animation = Animation()
            animation.width = 1
            animation.height = 1
            animation.frameCount = 3
            animation.endless = False
            animation.advanceByStep = False
            animation.frameColors = [
                weaponColor,
                weaponColor,
                weaponColor,
            ]
            animation.frameTime = [
                0.1,
                0.1,
                0.1
            ]

            animation.arr = [
                [
                    [ 'O', ],
                ],
                [
                    [ 'o', ],
                ],
                [
                    [ '.', ],
                ]
            ]

        if phenomenaType is PhenomenaType.hitSquare:
            animation = Animation()
            animation.width = 2
            animation.height = 2
            animation.frameCount = 3
            animation.endless = False
            animation.advanceByStep = False
            animation.frameColors = [
                weaponColor,
                weaponColor,
                weaponColor,
            ]
            animation.frameTime = [
                0.1,
                0.1,
                0.1
            ]

            animation.arr = [
                [
                    [ 'O', 'O' ],
                    [ 'O', 'O' ],
                ],
                [
                    [ 'o', 'o' ],
                    [ 'o', 'o' ],
                ],
                [
                    [ '.', '.' ],
                    [ '.', '.' ],
                ]
            ]

        if phenomenaType is PhenomenaType.hitLine:
            animation = Animation()
            animation.width = 4
            animation.height = 1
            animation.frameCount = 3
            animation.endless = False
            animation.advanceByStep = False
            animation.frameColors = [
                weaponColor,
                weaponColor,
                weaponColor,
            ]
            animation.frameTime = [
                0.1,
                0.1,
                0.1,
            ]

            if direction is Direction.right:
                animation.arr = [
                    [
                        [ '.', '', '', ''],
                    ],
                    [
                        [ '.', 'o', '', ''],
                    ],
                    [
                        [ '.', 'o', 'O', 'O'],
                    ]
                ]
            else:
                animation.arr = [
                    [
                        [ '', '', '', '.'],
                    ],
                    [
                        [ '', '', 'o', '.'],
                    ],
                    [
                        [ 'O', 'O', 'o', '.'],
                    ]
                ]

        if phenomenaType is PhenomenaType.roflcopter:
            animation = self.fileTextureLoader.readPhenomena('roflcopter')
            animation.endless = True
            animation.advanceByStep = False
            animation.frameColors = [
                ColorPalette.getColorByColor(Color.white),
                ColorPalette.getColorByColor(Color.white),
            ]
            animation.frameTime = [
                0.2,
                0.2
            ]

        if phenomenaType is PhenomenaType.intro:
            animation = self.fileTextureLoader.readPhenomena('intro')
            animation.endless = True
            animation.advanceByStep = False

            animation.frameTime = [
                0.1,
                0.5,
            ]
            animation.frameColors = [
                ColorPalette.getColorByColor(Color.brightblue),
                ColorPalette.getColorByColor(Color.white),
            ]

        if phenomenaType is PhenomenaType.tree1:
            animation = self.fileTextureLoader.readPhenomena('tree1')
            animation.endless = True
            animation.advanceByStep = False
            animation.frameTime = None
            animation.frameColors = [ mapColor, ]

        if phenomenaType is PhenomenaType.tree2:
            animation = self.fileTextureLoader.readPhenomena('tree2')
            animation.endless = True
            animation.advanceByStep = False
            animation.frameTime = None
            animation.frameColors = [ mapColor, ]

        if phenomenaType is PhenomenaType.tree3:
            animation = self.fileTextureLoader.readPhenomena('tree3')
            animation.endless = True
            animation.advanceByStep = False
            animation.frameTime = None
            animation.frameColors = [ mapColor, ]

        if phenomenaType is PhenomenaType.tree4:
            animation = self.fileTextureLoader.readPhenomena('tree4')
            animation.frameCount = 2
            animation.endless = True
            animation.advanceByStep = False
            animation.frameTime = [ 2.0, 2.0 ]
            animation.frameColors = [ mapColor, mapColor ]

        Utility.checkAnimation(animation, phenomenaType, None)

        return animation

