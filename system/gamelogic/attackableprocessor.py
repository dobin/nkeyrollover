import esper
import logging

from system.renderable import Renderable
from system.gamelogic.enemy import Enemy
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from utilities.utilities import Utility
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from system.gamelogic.ai import Ai
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType

logger = logging.getLogger(__name__)


class AttackableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        # if enemies have less than 0 health, make them gonna die
        for ent, (attackable, renderable, enemy, ai) in self.world.get_components(
            Attackable, Renderable, Enemy, Ai
        ):
            if attackable.getHealth() <= 0:
                if renderable.isActive(): # and/or: enemy.brain.state.name != 'idle' ?
                    ai.brain.pop()
                    ai.brain.push('dying')


        # damage taken
        msg = directMessaging.get(
            messageType = DirectMessageType.receiveDamage
        )
        while msg is not None:
            entity = Utility.findCharacterByGroupId(self.world, msg.groupId)
            meRenderable = self.world.component_for_entity(
                entity, Renderable)
            meAttackable = self.world.component_for_entity(
                entity, Attackable)
            damage = msg.data                

            if self.world.has_component(entity, Ai):
                meAi = self.world.component_for_entity(
                    entity, Ai)
                
                # put enemy it into state stun
                if meAi is not None:
                    if meAi.brain.state.name != 'stun':
                        meAi.brain.push('stun')
            else: 
                mePlayer = self.world.component_for_entity(
                    entity, Player)
                mePlayer.setState('stun')

            # play stun animation
            messaging.add(
                type=MessageType.EntityStun,
                data=None, 
                groupId=msg.groupId)

            # change health
            meAttackable.handleHit(damage)

            # color the texture
            meRenderable.texture.setOverwriteColorFor(
                1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))

            # get next message
            msg = directMessaging.get(
                messageType = DirectMessageType.receiveDamage
            )