import logging

from texture.texturetype import TextureType
from texture.action.actiontexture import ActionTexture
from texture.phenomena.phenomenatexture import PhenomenaTexture
from system.graphics.renderable import Renderable

logger = logging.getLogger(__name__)


class RenderableCache(object):
    def __init__(self, size=32):
        self.size = size
        self.viewport = None


    def init(self, viewport):
        self.viewport = viewport

        self.cache = {
            TextureType.action: [],
            TextureType.character: [],
            TextureType.phenomena: [],
            TextureType.speech: []
        }

        n = 0
        while n < self.size:
            texture = ActionTexture()
            renderable = Renderable(
                texture=texture,
                viewport=self.viewport,
                active=True,
                name="ActionRenderable init")
            self.addRenderable(renderable, TextureType.action)
            n += 1

        n = 0
        while n < self.size:
            texture = PhenomenaTexture()
            renderable = Renderable(
                texture=texture,
                viewport=self.viewport,
                active=True,
                name="PhenomenaRenderable init")
            self.addRenderable(renderable, TextureType.phenomena)
            n += 1
            

    def addRenderable(self, renderable, textureType):
        self.cache[textureType].append(renderable)


    def getRenderable(self, textureType):
        renderable = self.cache[textureType].pop(0)
        return renderable


renderableCache = RenderableCache()
