import logging

from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from system.graphics.renderable import Renderable
from common.coordinates import Coordinates

logger = logging.getLogger(__name__)


class EnvironmentOrchestrator(object):
    def __init__(self, viewport, mapManager):
        self.mapManager = mapManager
        self.viewport = viewport

        self.envRenderables = None
        self.activeEnvEntities = []

        self.loadEnvironment()


    def loadEnvironment(self):
        self.envRenderables = [None] * 800  # FIXME self.mapManager.getCurrentMapWidth()

        t = PhenomenaTexture(phenomenaType=PhenomenaType.puddle, setbg=True)
        r = Renderable(
            texture=t,
            viewport=self.viewport,
            coordinates=Coordinates(30, 10),
            active=True,
            name='Env Puddle'
        )
        self.addEnvRenderable(r)


    def addEnvRenderable(self, renderable :Renderable):
        x = renderable.getLocation().x
        if not self.envRenderables[x]:
            self.envRenderables[x] = []

        self.envRenderables[x].append(renderable)


    def trySpawn(self, world, newX):
        if newX < 0:
            return

        x = newX
        maxx = x + 78
        while x < maxx:
            if self.envRenderables[x] is not None:
                for renderable in self.envRenderables[x]:
                    logging.info("Add env {}".format(renderable))
                    entity = world.create_entity()
                    world.add_component(entity, renderable)
                    self.activeEnvEntities.append((entity, renderable))
                    self.envRenderables[x].remove(renderable)

            x += 1


    def tryRemoveOld(self, world, newX):
        if newX <= 0:
            return

        for entry in self.activeEnvEntities:
            entity = entry[0]
            renderable = entry[1]

            if renderable.getLocation().x < newX - 10:
                world.delete_entity(entity)
                self.activeEnvEntities.remove(entry)
