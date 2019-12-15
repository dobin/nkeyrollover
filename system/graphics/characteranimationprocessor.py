import esper
import logging
import random

from texture.character.characteranimationtype import CharacterAnimationType
from messaging import messaging, MessageType
import system.graphics.renderable
import system.gamelogic.player
from utilities.entityfinder import EntityFinder

logger = logging.getLogger(__name__)


class CharacterAnimationProcessor(esper.Processor):
    """Update the texture of renderable which are CharacterAnimations."""
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        self.checkForMove()
        self.checkForAttack()
        self.checkForStun()
        self.checkForDying()
        self.checkForKnockdown()


    def checkForKnockdown(self):
        for message in messaging.getByType(MessageType.EntityKnockdown):
            entity = EntityFinder.findCharacterByGroupId(self.world, message.groupId)
            meRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            meRenderable.texture.changeAnimation(
                characterAnimationType=CharacterAnimationType.knockdown,
                direction=meRenderable.direction,
                interrupt=True)


    def checkForDying(self):
        for message in messaging.getByType(MessageType.EntityDying):
            entity = EntityFinder.findCharacterByGroupId(self.world, message.groupId)
            meRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            animationIndex = random.randint(0, 1)
            meRenderable.texture.changeAnimation(
                characterAnimationType=CharacterAnimationType.dying,
                direction=meRenderable.direction,
                subtype=animationIndex,
                interrupt=False)


    def checkForMove(self):
        for message in messaging.getByType(MessageType.EntityMoved):
            entity = EntityFinder.findCharacterByGroupId(self.world, message.groupId)
            renderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            # just updated direction
            # NOTE this only works for CharacterTexture's
            if message.data['x'] == 0 and message.data['y'] == 0:
                renderable.texture.changeAnimation(
                    renderable.texture.characterAnimationType,
                    renderable.direction
                )
                continue

            if (renderable.texture.characterAnimationType
                    is CharacterAnimationType.walking):
                if message.data['didChangeDirection']:
                    renderable.texture.changeAnimation(
                        CharacterAnimationType.walking,
                        renderable.direction)
                else:
                    renderable.texture.advanceStep()
            else:
                renderable.texture.changeAnimation(
                    CharacterAnimationType.walking,
                    renderable.direction)


    def checkForAttack(self):
        messages = messaging.get()
        for message in messages:
            # PlayerAttack - Player
            if message.type == MessageType.PlayerAttack:
                playerEntity = EntityFinder.findPlayer(self.world)
                playerRenderable = self.world.component_for_entity(
                    playerEntity, system.graphics.renderable.Renderable)

                playerRenderable.texture.changeAnimation(
                    message.data['characterAttackAnimationType'],
                    playerRenderable.direction,
                    interrupt=True)

            # EntityAttack - Enemies
            if message.type == MessageType.EntityAttack:
                entity = EntityFinder.findCharacterByGroupId(
                    self.world, message.groupId)
                entityRenderable = self.world.component_for_entity(
                    entity, system.graphics.renderable.Renderable)

                entityRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitting,
                    entityRenderable.direction,
                    interrupt=True)

            # EntityAttack - Enemies
            if message.type == MessageType.EntityStanding:
                entity = EntityFinder.findCharacterByGroupId(
                    self.world, message.groupId)
                entityRenderable = self.world.component_for_entity(
                    entity, system.graphics.renderable.Renderable)

                entityRenderable.texture.changeAnimation(
                    CharacterAnimationType.standing,
                    entityRenderable.direction,
                    interrupt=True)

            # attackWindup- only for Enemies
            if message.type == MessageType.attackWindup:
                entity = EntityFinder.findCharacterByGroupId(
                    self.world, message.groupId)
                entityRenderable = self.world.component_for_entity(
                    entity, system.graphics.renderable.Renderable)

                entityRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitwindup,
                    entityRenderable.direction,
                    interrupt=True)


    def checkForStun(self):
        for message in messaging.getByType(MessageType.EntityStun):
            entity = EntityFinder.findCharacterByGroupId(self.world, message.groupId)
            entityRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            # here we also store the current animation
            # by interrupt=True
            entityRenderable.texture.changeAnimation(
                CharacterAnimationType.stun,
                entityRenderable.direction,
                interrupt=True)

        for message in messaging.getByType(MessageType.EntityEndStun):
            entity = EntityFinder.findCharacterByGroupId(self.world, message.groupId)
            entityRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            # restore saved animation
            entityRenderable.texture.previousAnimationRestore()
