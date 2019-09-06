import esper
import logging

from utilities.timer import Timer
from utilities.color import Color
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from world.viewport import Viewport
from sprite.coordinates import Coordinates
from system.renderableminimal import RenderableMinimal
from messaging import messaging, MessageType

logger = logging.getLogger(__name__)


class RenderableMinimalProcessor(esper.Processor):
    def __init__(self, viewport :Viewport, textureEmiter): 
        super().__init__()
        self.viewport = viewport
        self.textureEmiter = textureEmiter


    def process(self, dt):
        self.handleMessages()
        self.advance(dt)
        self.draw()


    def handleMessages(self):
        for message in messaging.getByType(MessageType.EmitTextureChar):
            self.textureEmiter.showCharAtPos(
                char = message.data['char'],
                timeout = message.data['timeout'],
                coordinate = message.data['coordinate'],
                color = message.data['color'],
            )


    def advance(self, dt):
        for ent, rend in self.world.get_component(RenderableMinimal):
            # advance it
            self.handleTextureChar(rend, dt)

            # remove it if inactive
            if not rend.isActive():
                self.world.delete_entity(ent)

    
    def handleTextureChar(self, rend, deltaTime):
        if not rend.isActive():
            return

        rend.advance(deltaTime)
        rend.texture.advance(deltaTime)

        if rend.texture.timer.timeIsUp():
            rend.texture.idx += 1

            if rend.texture.idx == len(rend.texture.timeArr):
                rend.setActive(False)
                return

            rend.texture.timer.setTimer(rend.texture.timeArr[ rend.texture.idx ])
            rend.texture.timer.start()
            rend.coordinates.x += rend.texture.movementX
            rend.coordinates.y += rend.texture.movementY


    def draw(self):
        for ent, rend in self.world.get_component(RenderableMinimal):
            self.drawMinimalRenderable(rend)


    def drawMinimalRenderable(self, rend):
        if not rend.isActive():
            return

        color = rend.texture.colorArr[ rend.texture.idx ]

        self.viewport.addstr(
                rend.coordinates.y,
                rend.coordinates.x,
                rend.texture.char,
                color)

