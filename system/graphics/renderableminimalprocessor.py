import esper
import logging

from game.viewport import Viewport
from system.graphics.renderableminimal import RenderableMinimal
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
        for message in messaging.getByType(MessageType.EmitTextureMinimal):
            self.textureEmiter.showCharAtPos(
                char = message.data['char'],
                timeout = message.data['timeout'],
                coordinate = message.data['coordinate'],
                color = message.data['color'],
            )

        for message in messaging.getByType(MessageType.EmitTexture):
            self.textureEmiter.showEffect(
                effect = message.data['effect'],
                pos = message.data['pos'],
                frame = message.data['frame'],
                charDirection = message.data['charDirection'],
            )

        for message in messaging.getByType(MessageType.EmitActionTexture):
            self.textureEmiter.makeActionTexture(
                actionTextureType = message.data['actionTextureType'],
                location = message.data['location'],
                fromPlayer = message.data['fromPlayer'],
                direction = message.data['direction'],
                physics = message.data['physics'],
            )

        for message in messaging.getByType(MessageType.EmitPhenomenaTexture):
            self.textureEmiter.makePhenomenaTexture(
                phenomenaTextureType = message.data['phenomenaTextureType'],
                location = message.data['location'],
                staticLocation = message.data['staticLocation'],
                direction = message.data['direction'],
                physics = message.data['physics'],
            )


    def advance(self, dt):
        for ent, rend in self.world.get_component(RenderableMinimal):
            # advance it
            self.handleTextureMinimal(rend, dt)

            # remove it if inactive
            if not rend.isActive():
                logger.info("Remove Entity F: {}".format(ent))
                self.world.delete_entity(ent)


    def handleTextureMinimal(self, rend, deltaTime):
        if not rend.isActive():
            return

        rend.advance(deltaTime)
        rend.texture.advance(deltaTime)

        if rend.texture.timer.timeIsUp():
            rend.texture.idx += 1

            if rend.texture.idx == len(rend.texture.timeArr):
                rend.setActive(False)
                return

            rend.texture.timer.setTimer(rend.texture.timeArr[rend.texture.idx])
            rend.texture.timer.start()
            rend.coordinates.x += rend.texture.movementX
            rend.coordinates.y += rend.texture.movementY


    def draw(self):
        for ent, rend in self.world.get_component(RenderableMinimal):
            self.drawMinimalRenderable(rend)


    def drawMinimalRenderable(self, rend):
        if not rend.isActive():
            return

        color = rend.texture.colorArr[rend.texture.idx]

        self.viewport.addstr(
            rend.coordinates.y,
            rend.coordinates.x,
            rend.texture.char,
            color=color[0],
            attr=color[1])
