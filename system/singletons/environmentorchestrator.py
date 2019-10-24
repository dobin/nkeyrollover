import logging
import random

from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from system.graphics.renderable import Renderable
from common.coordinates import Coordinates
from system.gamelogic.attackable import Attackable
import game.uniqueid
from system.groupid import GroupId

logger = logging.getLogger(__name__)


class EnvironmentOrchestrator(object):
    def __init__(self, viewport, mapManager):
        self.mapManager = mapManager
        self.viewport = viewport

        self.envRenderables = None
        self.activeEnvEntities = []

        self.loadEnvironment()


    def loadEnvironment(self):
        width = 800  # FIXME self.mapManager.getCurrentMapWidth()
        self.envRenderables = [None] * width


        n = random.randrange(30, 60)
        while n < width - 100:
            t = PhenomenaTexture(phenomenaType=PhenomenaType.puddle, setbg=True)
            x = n
            y = random.randrange(10, 20)
            r = Renderable(
                texture=t,
                viewport=self.viewport,
                coordinates=Coordinates(x, y),
                active=True,
                name='Env Puddle'
            )
            attackable = Attackable(
                initialHealth=40,
                stunCount=0,
                stunTimeFrame=0.0,
                stunTime=0,
                knockdownChance=0.0,
                knockbackChance=0.0)
            groupId = GroupId(id=game.uniqueid.getUniqueId())
            self.addEnvRenderable(r, attackable, groupId)

            n += random.randrange(30, 60)


    def addEnvRenderable(
        self, renderable :Renderable, attackable :Attackable, groupId :GroupId
    ):
        x = renderable.getLocation().x
        if not self.envRenderables[x]:
            self.envRenderables[x] = []

        self.envRenderables[x].append((renderable, attackable, groupId))


    def trySpawn(self, world, newX):
        if newX < 0:
            return

        x = newX
        maxx = x + 78
        while x < maxx:
            if self.envRenderables[x] is not None:
                for entry in self.envRenderables[x]:
                    logging.info("Add env {}".format(entry))
                    renderable = entry[0]
                    attackable = entry[1]
                    groupId = entry[2]

                    entity = world.create_entity()
                    world.add_component(entity, renderable)
                    world.add_component(entity, attackable)
                    world.add_component(entity, groupId)
                    self.activeEnvEntities.append((entity, renderable, attackable, groupId))
                    self.envRenderables[x].remove(entry)

            x += 1


    def tryRemoveOld(self, world, newX):
        if newX <= 0:
            return

        for entry in self.activeEnvEntities:
            entity = entry[0]
            renderable = entry[1]
            attackable = entry[2]

            if attackable.getHealth() <= 0:
                world.delete_entity(entity)
                self.activeEnvEntities.remove(entry)

            if renderable.getLocation().x < newX - 10:
                world.delete_entity(entity)
                self.activeEnvEntities.remove(entry)
