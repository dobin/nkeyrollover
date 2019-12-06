import logging

from system.graphics.renderable import Renderable
import system.gamelogic.offensiveattack
import system.gamelogic.offensiveskill
import system.gamelogic.attackable
import system.graphics.renderable
import system.graphics.physics
import system.groupid

logger = logging.getLogger(__name__)


class EntityFinder(object):
    @staticmethod
    def isDestinationEmpty(world, renderable :Renderable) -> bool:
        """Check if renderable/extCoords overlaps with any other renderables"""
        for ent, (otherRend, physics) in world.get_components(
            system.graphics.renderable.Renderable,
            system.graphics.physics.Physics
        ):
            dist = otherRend.distanceToBorder(renderable)
            # fast check: distance
            if dist['x'] <= 0 and dist['y'] <= 0:
                if not renderable == otherRend:
                    # slower check: overlap
                    overlap = otherRend.overlapsWith(renderable)
                    if overlap:
                        # slowest: pixel perfect check
                        overlap = otherRend.overlapsWithRenderablePixel(renderable)
                        if overlap:
                            logger.info("{} Cant go to {}/{} because {}".format(
                                renderable,
                                renderable.coordinates.x,
                                renderable.coordinates.y,
                                otherRend
                            ))
                            return False

        return True


    @staticmethod
    def isDestinationWithPlayer(world, renderable :Renderable) -> bool:
        playerEntity = EntityFinder.findPlayer(world)
        otherRend = world.component_for_entity(playerEntity, Renderable)

        dist = otherRend.distanceToBorder(renderable)
        # fast check: distance
        if dist['x'] <= 0 and dist['y'] <= 0:
            if not renderable == otherRend:
                # slower check: overlap
                overlap = otherRend.overlapsWith(renderable)
                if overlap:
                    # slowest: pixel perfect check
                    overlap = otherRend.overlapsWithRenderablePixel(renderable)
                    if overlap:
                        return True

        return False


    @staticmethod
    def isDestinationEmptyForParticle(world, particle) -> bool:
        """Check if renderable/extCoords overlaps with any other renderables"""
        for ent, (otherRend, physics) in world.get_components(
            system.graphics.renderable.Renderable,
            system.graphics.physics.Physics
        ):
            if otherRend.distanceToPoint(particle.x, particle.y) <= 0:
                if otherRend.overlapsWithPointPixel(particle.x, particle.y):
                    return False

        return True


    @staticmethod
    def findByGroupId(world, id):
        for ent, (groupId, renderable) in world.get_components(
            system.groupid.GroupId,
            system.graphics.renderable.Renderable,
        ):
            if groupId.getId() == id:
                return ent


    @staticmethod
    def findAttackableByGroupId(world, id):
        for ent, (groupId, renderable, attackable) in world.get_components(
            system.groupid.GroupId,
            system.graphics.renderable.Renderable,
            system.gamelogic.attackable.Attackable,
        ):
            if groupId.getId() == id:
                return ent


    @staticmethod
    def findCharacterByGroupId(world, id):
        for ent, (groupId, renderable, player) in world.get_components(
            system.groupid.GroupId,
            system.graphics.renderable.Renderable,
            system.gamelogic.player.Player,
        ):
            if groupId.getId() == id:
                return ent

        for ent, (groupId, renderable, enemy) in world.get_components(
            system.groupid.GroupId,
            system.graphics.renderable.Renderable,
            system.gamelogic.enemy.Enemy,
        ):
            if groupId.getId() == id:
                return ent

        logger.error("Could not find entity with groupId: {}".format(
            id
        ))


    @staticmethod
    def findOffensiveAttackByGroupId(world, id):
        for ent, (groupId, offensiveAttack) in world.get_components(
            system.groupid.GroupId,
            system.gamelogic.offensiveattack.OffensiveAttack
        ):
            if groupId.getId() == id:
                return offensiveAttack

        logger.error("Could not find offensive attack with groupId: {}".format(
            id
        ))
        return None


    @staticmethod
    def findOffensiveSkillByGroupId(world, id):
        for ent, (groupId, offensiveSkill) in world.get_components(
            system.groupid.GroupId,
            system.gamelogic.offensiveskill.OffensiveSkill
        ):
            if groupId.getId() == id:
                return offensiveSkill

        logger.error("Could not find offensive attack with groupId: {}".format(
            id
        ))
        return None


    @staticmethod
    def findPlayer(world):
        for ent, player, in world.get_component(
            system.gamelogic.player.Player,
        ):
            return ent


    @staticmethod
    def numEnemiesInState(world, state):
        num = 0
        for ent, ai in world.get_component(
            system.gamelogic.ai.Ai,
        ):
            if ai.brain.state.name == state:
                num += 1

        return num

    @staticmethod
    def numEnemies(world): 
        num = 0
        for ent, ai in world.get_component(
            system.gamelogic.ai.Ai,
        ):
            num += 1

        return num
