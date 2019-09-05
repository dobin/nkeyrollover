import esper
import logging
import random

from system.renderable import Renderable
from system.groupid import GroupId
from system.gamelogic.enemy import Enemy
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from utilities.utilities import Utility
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from system.gamelogic.ai import Ai
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.entityfinder import EntityFinder

logger = logging.getLogger(__name__)


class AttackableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        self.checkHealth()
        self.checkReceiveDamage() # dont stun if he has no health left..
                
        self.advance(dt)


    def advance(self, dt): 
        for ent, meAttackable in self.world.get_component(
            Attackable
        ):
            # advance timers
            meAttackable.advance(dt)

            # check if stun is finished
            if meAttackable.stunTimer.timeIsUp(): 
                meAttackable.isStunned = False
                meAttackable.stunTimer.stop()

                # generate end stun message (for animation)
                # ?


    def checkHealth(self):
        # if enemies have less than 0 health, make them gonna die
        for ent, (attackable, meRenderable, meEnemy, ai, meGroupId) in self.world.get_components(
            Attackable, Renderable, Enemy, Ai, GroupId
        ):
            if attackable.getHealth() <= 0:
                if ai.brain.state.name is not 'idle' and ai.brain.state.name is not 'dying':
                    # update state
                    ai.brain.pop()
                    ai.brain.push('dying')

                    messaging.add(
                        type = MessageType.EntityDying,
                        groupId = meGroupId.getId(),
                        data = {}
                    )


    def checkReceiveDamage(self):
        # damage taken
        msg = directMessaging.get(
            messageType = DirectMessageType.receiveDamage
        )
        while msg is not None:
            entity = EntityFinder.findCharacterByGroupId(self.world, msg.groupId)
            meRenderable = self.world.component_for_entity(
                entity, Renderable)
            meAttackable = self.world.component_for_entity(
                entity, Attackable)
            meGroupId = self.world.component_for_entity(
                entity, GroupId)
            damage = msg.data                

            # change health
            meAttackable.handleHit(damage)

            # dont stun if there is no health left
            if meAttackable.getHealth() > 0.0:
                stunTime = 0.75
                meAttackable.stunTimer.setTimer(timerValue=stunTime)
                meAttackable.stunTimer.start()
                meAttackable.isStunned = True

                messaging.add(
                    type=MessageType.EntityStun,
                    data={
                        'timerValue': stunTime,
                    },
                    groupId = meGroupId.getId(),
                )

            # color the texture, even if we are dead
            meRenderable.texture.setOverwriteColorFor(
                1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))

            # get next message
            msg = directMessaging.get(
                messageType = DirectMessageType.receiveDamage
            )