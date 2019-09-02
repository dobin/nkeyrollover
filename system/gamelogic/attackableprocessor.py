import esper
import logging

from system.renderable import Renderable
from system.gamelogic.enemy import Enemy
from system.gamelogic.attackable import Attackable
from utilities.utilities import Utility
from directmessaging import directMessaging, DirectMessageType
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from system.gamelogic.ai import Ai

logger = logging.getLogger(__name__)


class AttackableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        # if enemies have taken enough damage, make them gonna die
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

            # xxx.changeState(stun)
            meAttackable.handleHit(damage)
            meRenderable.setOverwriteColorFor(
                1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))

            # get next message
            msg = directMessaging.get(
                messageType = DirectMessageType.receiveDamage
            )