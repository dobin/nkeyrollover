import esper
import logging
import random

from texture.character.characteranimationtype import CharacterAnimationType
from messaging import messaging, MessageType
import system.graphics.renderable
import system.gamelogic.player
from utilities.entityfinder import EntityFinder
from world.textureemiter import TextureEmiterEffect

logger = logging.getLogger(__name__)


class CharacterAnimationProcessor(esper.Processor):
    """Update the texture of renderable which are CharacterAnimations.

    Accesses events:
    * MessageType.EntityMoved
    * MessageType.PlayerAttack
    * MessageType.attackWindup
    * MessageType.EntityAttack
    """
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        self.animationUpdateMove()
        self.animationUpdateAttack()
        self.animationUpdateStun()
        self.animationUpdateDying()


    def animationUpdateDying(self):
        for message in messaging.getByType(MessageType.EntityDying):
            entity = EntityFinder.findCharacterByGroupId(self.world, message.groupId)
            meRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            if random.choice([True, False]):
                logger.info(meRenderable.name + " Death animation deluxe")
                animationIndex = random.randint(0, 1)

                effect = random.choice(
                    [TextureEmiterEffect.explode, TextureEmiterEffect.pushback])
                messaging.add(
                    type=MessageType.EmitTexture,
                    data = {
                        'effect': effect,
                        'pos': meRenderable.getLocation(),
                        'frame': meRenderable.texture.getCurrentFrameCopy(),
                        'charDirection': meRenderable.direction,                        
                    }
                )

                # really necessary? it is disabled..
                # should be before message add, to get frame copy of dead animation?
                meRenderable.texture.changeAnimation(
                    CharacterAnimationType.dying,
                    meRenderable.direction,
                    animationIndex)
                meRenderable.setActive(False)

            else:
                animationIndex = random.randint(0, 1)
                meRenderable.texture.changeAnimation(
                    CharacterAnimationType.dying,
                    meRenderable.direction,
                    animationIndex)


    def animationUpdateMove(self):
        for message in messaging.getByType(MessageType.EntityMoved):
            entity = EntityFinder.findCharacterByGroupId(self.world, message.groupId)
            renderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

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


    def animationUpdateAttack(self):
        messages = messaging.get()
        for message in messages:
            if message.type == MessageType.PlayerAttack:
                playerEntity = EntityFinder.findPlayer(self.world)
                playerRenderable = self.world.component_for_entity(
                    playerEntity, system.graphics.renderable.Renderable)

                playerRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitting,
                    playerRenderable.direction)

            if message.type == MessageType.attackWindup:
                entity = EntityFinder.findCharacterByGroupId(
                    self.world, message.groupId)
                entityRenderable = self.world.component_for_entity(
                    entity, system.graphics.renderable.Renderable)

                entityRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitwindup,
                    entityRenderable.direction)

            if message.type == MessageType.EntityAttack:
                entity = EntityFinder.findCharacterByGroupId(
                    self.world, message.groupId)
                entityRenderable = self.world.component_for_entity(
                    entity, system.graphics.renderable.Renderable)

                entityRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitting,
                    entityRenderable.direction)


    def animationUpdateStun(self): 
        for message in messaging.getByType(MessageType.EntityStun):
            entity = EntityFinder.findCharacterByGroupId(self.world, message.groupId)
            entityRenderable = self.world.component_for_entity(
                entity, system.graphics.renderable.Renderable)

            entityRenderable.texture.changeAnimation(
                CharacterAnimationType.stun,
                entityRenderable.direction)
