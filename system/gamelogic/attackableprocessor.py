import esper
import logging
import random

from system.graphics.renderable import Renderable
from system.groupid import GroupId
from system.gamelogic.enemy import Enemy
from system.gamelogic.attackable import Attackable
from system.gamelogic.player import Player
from system.gamelogic.ai import Ai
from utilities.colorpalette import ColorPalette
from utilities.color import Color
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
from utilities.entityfinder import EntityFinder
from game.textureemiter import TextureEmiterEffect
from system.graphics.particleeffecttype import ParticleEffectType
from config import Config
from common.direction import Direction

logger = logging.getLogger(__name__)


class AttackableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        self.checkHealth()
        self.checkReceiveDamage()  # dont stun if he has no health left..
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

                # generate end-stun message (for animation)
                # ?


    def checkHealth(self):
        # if enemies have less than 0 health, make them gonna die
        for ent, (meAtk, meEnemy, ai, meGroupId, meRend) in self.world.get_components(
            Attackable, Enemy, Ai, GroupId, Renderable
        ):
            if meAtk.getHealth() <= 0:
                if ai.brain.state.name != 'dead' and ai.brain.state.name != 'dying':
                    # update state
                    ai.brain.pop()
                    ai.brain.push('dying')

                    messaging.add(
                        type = MessageType.EntityDying,
                        groupId = meGroupId.getId(),
                        data = {}
                    )

                    # 50% chance to display a fancy death animation
                    if random.choice([True, False]):
                        logger.info(meRend.name + " Death animation deluxe")

                        effect = random.choice(
                            [TextureEmiterEffect.explode, TextureEmiterEffect.pushback])
                        messaging.add(
                            type=MessageType.EmitTexture,
                            data = {
                                'effect': effect,
                                'pos': meRend.getLocation(),
                                'frame': meRend.texture.getCurrentFrameCopy(),
                                'charDirection': meRend.direction,
                            }
                        )

                        meRend.setActive(False)


    def checkReceiveDamage(self):
        for msg in directMessaging.getByType(DirectMessageType.receiveDamage):
            entity = EntityFinder.findCharacterByGroupId(self.world, msg.groupId)
            if entity is None:
                # May be already deleted?
                continue

            meRenderable = self.world.component_for_entity(
                entity, Renderable)
            meAttackable = self.world.component_for_entity(
                entity, Attackable)
            meGroupId = self.world.component_for_entity(
                entity, GroupId)
            damage = msg.data['damage']
            byPlayer = msg.data['byPlayer']
            direction = msg.data['direction']
            isPlayer = self.world.has_component(entity, Player)

            # enemy can attack player, and vice-versa
            if not byPlayer ^ isPlayer:
                continue

            # change health
            meAttackable.adjustHealth(-1 * damage)

            # dont stun if there is no health left
            if meAttackable.getHealth() > 0.0:
                if meAttackable.isStunnable():
                    stunTime = meAttackable.stunTime
                    meAttackable.stunTimer.setTimer(timerValue=stunTime)
                    meAttackable.stunTimer.start()
                    meAttackable.isStunned = True
                    meAttackable.addStun(stunTime=stunTime)

                    messaging.add(
                        type=MessageType.EntityStun,
                        data={
                            'timerValue': stunTime,
                        },
                        groupId = meGroupId.getId(),
                    )

                healthPercentage = meAttackable.getHealthPercentage()
                # color the texture if we are not dead
                if healthPercentage > 0.5:
                    meRenderable.texture.setOverwriteColorFor(
                        0.1, ColorPalette.getColorByColor(Color.yellow))
                else:
                    meRenderable.texture.setOverwriteColorFor(
                        0.1, ColorPalette.getColorByColor(Color.red))

                if Config.showEnemyDamageNumbers:
                    messaging.add(
                        type=MessageType.EmitParticleEffect,
                        data= {
                            'location': meRenderable.getLocationTopCenter(),
                            'effectType': ParticleEffectType.floatingDamage,
                            'damage': damage,
                            'byPlayer': byPlayer,
                            'direction': Direction.none,
                        }
                    )

                if Config.showBurstOnImpact:
                    if damage > Config.showBurstOnImpactDamage:
                        messaging.add(
                            type=MessageType.EmitParticleEffect,
                            data= {
                                'location': meRenderable.getAttackBaseLocationInverted(),
                                'effectType': ParticleEffectType.hitBurst,
                                'damage': 0,
                                'byPlayer': byPlayer,
                                'direction': direction,
                            }
                        )