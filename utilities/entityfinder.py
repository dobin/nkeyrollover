import logging

import system.offensiveattack
import system.offensiveskill
import system.gamelogic.attackable
import system.renderable
import system.groupid

logger = logging.getLogger(__name__)


class EntityFinder(object): 
    @staticmethod
    def findCharacterByGroupId(world, id):
        for ent, (groupId, renderable, player) in world.get_components(
            system.groupid.GroupId,
            system.renderable.Renderable,
            system.gamelogic.player.Player,
        ):
            if groupId.getId() == id:
                return ent

        for ent, (groupId, renderable, enemy) in world.get_components(
            system.groupid.GroupId,
            system.renderable.Renderable,
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
            system.offensiveattack.OffensiveAttack
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
            system.offensiveskill.OffensiveSkill
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

