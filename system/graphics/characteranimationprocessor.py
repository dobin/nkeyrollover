import esper
import logging

from utilities.utilities import Utility
from texture.character.characteranimationtype import CharacterAnimationType
from messaging import messaging, MessageType
import system.advanceable
import system.renderable
import system.gamelogic.player

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


    def animationUpdateMove(self):
        messages = messaging.get()
        for msg in messages:
            if msg.type == MessageType.EntityMoved:
                entity = Utility.findCharacterByGroupId(self.world, msg.groupId)
                renderable = self.world.component_for_entity(
                    entity, system.renderable.Renderable)

                if renderable.texture.characterAnimationType is CharacterAnimationType.walking:
                    if msg.data['didChangeDirection']:
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
                playerEntity = Utility.findPlayer(self.world)
                playerRenderable = self.world.component_for_entity(
                    playerEntity, system.renderable.Renderable)

                playerRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitting,
                    playerRenderable.direction)

            if message.type == MessageType.attackWindup:
                entity = Utility.findCharacterByGroupId(self.world, message.groupId)
                entityRenderable = self.world.component_for_entity(
                    entity, system.renderable.Renderable)

                entityRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitwindup,
                    entityRenderable.direction)

            if message.type == MessageType.EntityAttack:
                entity = Utility.findCharacterByGroupId(self.world, message.groupId)
                entityRenderable = self.world.component_for_entity(
                    entity, system.renderable.Renderable)

                entityRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitting,
                    entityRenderable.direction)