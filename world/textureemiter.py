import logging
import random

from world.viewport import Viewport
from sprite.coordinates import Coordinates
from sprite.direction import Direction
from utilities.color import Color
from utilities.colorpalette import ColorPalette
from system.renderableminimal import RenderableMinimal, TextureChar

logger = logging.getLogger(__name__)


class TextureEmiter(object):
    def __init__(self, viewport :Viewport, esperWorld):
        self.viewport :Viewport = viewport
        self.esperWorld = esperWorld


    def showCharAtPos(self, char :str, timeout :float, coordinate :Coordinates, color :Color):
        textureChar = TextureChar(
            char=char,
            colorArr=[ColorPalette.getColorByColor( Color.brightyellow )],
            timeArr= [ timeout ],
        )
        renderableMinimal = RenderableMinimal(
            texture=textureChar,
            coordinate=coordinate,
        )

        self.addRenderableMinimal(renderableMinimal)


    def makeExplode(self, pos, frame, charDirection, data):
        effect = random.randint(1, 2)

        columnCount = len(frame)
        for (y, rows) in enumerate(frame):
            rowCnt = len(rows)

            for (x, column) in enumerate(rows):
                if column is not '':
                    self.makeEffect(effect, pos, x, y, column, columnCount, rowCnt, charDirection)


    def makeEffect(self, effect, pos, x, y, char, columnCount, rowCnt, charDirection):
        # explode
        if effect == 1:
            movementX = 0
            movementY = 0

            if y == 0:
                movementY = -1
            if x == 0:
                movementX = -1

            if y == columnCount - 1:
                movementY = 1
            if x == rowCnt - 1:
                movementX = 1

            c = Coordinates(
                x = pos.x + x,
                y = pos.y + y,
            )

            timeArr = [
                0.1,
                0.1,
                0.1
            ]
            colorArr = [
                ColorPalette.getColorByColor( Color.brightyellow ),
                ColorPalette.getColorByColor( Color.yellow ),
                ColorPalette.getColorByColor( Color.grey ),
            ]

            textureChar = TextureChar(
                char=char,
                movementX=movementX,
                movementY=movementY,
                timeArr=timeArr,
                colorArr=colorArr)
            renderableMinimal = RenderableMinimal(
                texture=textureChar,
                coordinate=c,
            )
            self.addRenderableMinimal(renderableMinimal)

        # push away
        if effect == 2:
            if charDirection is Direction.right:
                d = -1
            else:
                d = 1

            c = Coordinates(
                x = pos.x + x,
                y = pos.y + y,
            )

            timeArr = [
                0.05,
                0.1,
                0.2,
                0.4
            ]
            colorArr = [
                ColorPalette.getColorByColor( Color.white ),
                ColorPalette.getColorByColor( Color.white ),
                ColorPalette.getColorByColor( Color.grey ),
                ColorPalette.getColorByColor( Color.grey ),
            ]

            textureChar = TextureChar(
                char=char,
                movementX = d * 2,
                movementY = 0,
                timeArr=timeArr,
                colorArr=colorArr)
            renderableMinimal = RenderableMinimal(
                texture=textureChar,
                coordinate=c
            )
            self.addRenderableMinimal(renderableMinimal)


    def addRenderableMinimal(self, sprite):
        entity = self.esperWorld.create_entity()
        self.esperWorld.add_component(entity, sprite)
