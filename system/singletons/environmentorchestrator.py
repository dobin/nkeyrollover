import logging
import random

from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from system.graphics.renderable import Renderable
from system.graphics.physics import Physics
from common.coordinates import Coordinates
from system.gamelogic.attackable import Attackable
import game.uniqueid
from system.groupid import GroupId
from system.gamelogic.passiveattack import PassiveAttack

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

        # boxes
        t = PhenomenaTexture(phenomenaType=PhenomenaType.box, setbg=True)
        x = 30
        y = 15
        r = Renderable(
            texture=t,
            viewport=self.viewport,
            coordinates=Coordinates(x, y),
            active=True,
            name='Env Box',
            z=1,  # background
        )
        attackable = Attackable(
            initialHealth=40,
            stunCount=0,
            stunTimeFrame=0.0,
            stunTime=0,
            knockdownChance=0.0,
            knockbackChance=0.0)
        physics = Physics()
        groupId = GroupId(id=game.uniqueid.getUniqueId())
        self.addEnvRenderable(r, attackable, groupId, physics, None)

        # puddles
        if True:
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
                    name='Env Puddle',
                    z=1,  # background
                )
                p = PassiveAttack([10, 10])
                groupId = GroupId(id=game.uniqueid.getUniqueId())
                self.addEnvRenderable(r, None, groupId, None, p)

                n += random.randrange(30, 60)
        else:
            t = PhenomenaTexture(phenomenaType=PhenomenaType.puddle, setbg=True)
            x = 10
            y = 10
            r = Renderable(
                texture=t,
                viewport=self.viewport,
                coordinates=Coordinates(x, y),
                active=True,
                name='Env Puddle 10 10',
                z=1,  # background
            )
            p = PassiveAttack([10, 10])
            groupId = GroupId(id=game.uniqueid.getUniqueId())
            self.addEnvRenderable(r, None, groupId, None, p)



    def addEnvRenderable(
        self,
        renderable :Renderable,
        attackable :Attackable,
        groupId :GroupId,
        physics,
        passiveAttack,
    ):
        x = renderable.getLocation().x
        if not self.envRenderables[x]:
            self.envRenderables[x] = []

        self.envRenderables[x].append((renderable, attackable, groupId, physics, passiveAttack))


    def trySpawn(self, world, newX):
        if newX < 0:
            return

        x = newX
        maxx = x + 78
        while x < maxx:
            if self.envRenderables[x] is not None:
                for entry in self.envRenderables[x]:
                    logger.info("Add to env: {}".format(entry[0]))
                    renderable = entry[0]
                    attackable = entry[1]
                    groupId = entry[2]
                    physics = entry[3]
                    passiveAttack = entry[4]

                    entity = world.create_entity()
                    world.add_component(entity, renderable)
                    world.add_component(entity, groupId)
                    if attackable is not None:
                        world.add_component(entity, attackable)
                    if physics is not None:
                        world.add_component(entity, physics)
                    if passiveAttack is not None:
                        logger.info("Add to env {}: passive attack".format(entry[0]))
                        world.add_component(entity, passiveAttack)

                    self.activeEnvEntities.append((entity, renderable, attackable, groupId))
                    self.envRenderables[x].remove(entry)

            x += 1


    def tryRemoveOld(self, world, newX):
        if newX <= 0:
            return

        for entry in self.activeEnvEntities:
            entity = entry[0]
            renderable = entry[1]

            # attackable = entry[2]
            # if attackable.getHealth() <= 0:
            #    world.delete_entity(entity)  # done atm in renderableprocessor
            #    self.activeEnvEntities.remove(entry)

            if renderable.getLocation().x < newX - 10:
                world.delete_entity(entity)
                self.activeEnvEntities.remove(entry)
