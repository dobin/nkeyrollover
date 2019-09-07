import logging
from enum import Enum

from world.viewport import Viewport
from sprite.coordinates import Coordinates
from sprite.direction import Direction
from utilities.color import Color
from utilities.colorpalette import ColorPalette
from system.graphics.renderableminimal import RenderableMinimal
from system.graphics.textureminimal import TextureMinimal
from system.graphics.renderable import Renderable
from texture.action.actiontexture import ActionTexture
from messaging import messaging, MessageType
from texture.speech.speechtexture import SpeechTexture

logger = logging.getLogger(__name__)


class TextureEmiterEffect(Enum):
    explode = 0
    pushback = 1


class TextureEmiter(object):
    def __init__(self, viewport :Viewport, world):
        self.viewport :Viewport = viewport
        self.world = world


    def showSpeechBubble(self, displayText, time, parentRenderable):
        texture = SpeechTexture(
            displayText=displayText,
            time=time
        )
        coordinates = Coordinates(1, -4)
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=parentRenderable,
            coordinates=coordinates,
            z=3,
            active=True)
        self.addRenderable(renderable)


    def makeActionTexture(
        self, actionTextureType, location, fromPlayer, direction, damage=None
    ):
        texture :ActionTexture = ActionTexture(
            actionType=actionTextureType,
            direction=direction)

        if direction is Direction.left:
            location.x -= texture.width

        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=location,
            active=True)
        self.addRenderable(renderable)

        if damage is not None:
            hitLocations = renderable.getTextureHitCoordinates()

            msgType = None
            if fromPlayer:
                msgType = MessageType.PlayerAttack
            else:
                msgType = MessageType.EnemyAttack

            messaging.add(
                type=msgType,
                data={
                    'hitLocations': hitLocations,
                    'damage': damage,
                }
            )


    def addRenderable(self, renderable):
        entity = self.world.create_entity()
        self.world.add_component(entity, renderable)


    def showCharAtPos(
        self, char :str, timeout :float, coordinate :Coordinates, color :Color
    ):
        textureMinimal = TextureMinimal(
            char=char,
            colorArr=[ColorPalette.getColorByColor(color)],
            timeArr=[timeout],
        )
        renderableMinimal = RenderableMinimal(
            texture=textureMinimal,
            coordinate=coordinate,
        )

        self.addRenderableMinimal(renderableMinimal)


    def showEffect(self, pos, frame, charDirection, effect):
        columnCount = len(frame)
        for (y, rows) in enumerate(frame):
            rowCnt = len(rows)

            for (x, column) in enumerate(rows):
                if column != '':
                    self.makeEffect(
                        effect, pos, x, y, column, columnCount, rowCnt, charDirection)


    def makeEffect(self, effect, pos, x, y, char, columnCount, rowCnt, charDirection):
        if effect is TextureEmiterEffect.explode:
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
                x=pos.x + x,
                y=pos.y + y,
            )

            timeArr = [
                0.1,
                0.1,
                0.1
            ]
            colorArr = [
                ColorPalette.getColorByColor(Color.brightyellow),
                ColorPalette.getColorByColor(Color.yellow),
                ColorPalette.getColorByColor(Color.grey),
            ]

            textureMinimal = TextureMinimal(
                char=char,
                movementX=movementX,
                movementY=movementY,
                timeArr=timeArr,
                colorArr=colorArr)
            renderableMinimal = RenderableMinimal(
                texture=textureMinimal,
                coordinate=c,
            )
            self.addRenderableMinimal(renderableMinimal)

        # push away
        if effect is TextureEmiterEffect.pushback:
            if charDirection is Direction.right:
                d = -1
            else:
                d = 1

            c = Coordinates(
                x=pos.x + x,
                y=pos.y + y,
            )

            timeArr = [
                0.05,
                0.1,
                0.2,
                0.4
            ]
            colorArr = [
                ColorPalette.getColorByColor(Color.white),
                ColorPalette.getColorByColor(Color.white),
                ColorPalette.getColorByColor(Color.grey),
                ColorPalette.getColorByColor(Color.grey),
            ]

            textureMinimal = TextureMinimal(
                char=char,
                movementX=d * 2,
                movementY=0,
                timeArr=timeArr,
                colorArr=colorArr)
            renderableMinimal = RenderableMinimal(
                texture=textureMinimal,
                coordinate=c
            )
            self.addRenderableMinimal(renderableMinimal)


    def addRenderableMinimal(self, renderable):
        entity = self.world.create_entity()
        self.world.add_component(entity, renderable)
