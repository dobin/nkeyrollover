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
        for ent, (meAttackable, meGroupId) in self.world.get_components(
            Attackable, GroupId
        ):
            # advance timers
            meAttackable.advance(dt)

            # check if stun is finished
            if meAttackable.stunTimer.timeIsUp():
                meAttackable.isStunned = False
                meAttackable.stunTimer.stop()

                # generate end-stun message (for animation)
                messaging.add(
                    type = MessageType.EntityEndStun,
                    groupId = meGroupId.getId(),
                    data = {}
                )


    def checkHealth(self):
        # player
        playerEntity = EntityFinder.findPlayer(self.world)
        if playerEntity is not None:
            player = self.world.component_for_entity(
                playerEntity, Player)

            if player.isAlive:
                playerAttackable = self.world.component_for_entity(
                    playerEntity, Attackable)
                playerGroupId = self.world.component_for_entity(
                    playerEntity, GroupId)

                if playerAttackable.isActive and playerAttackable.getHealth() <= 0:
                    player.setAlive(False)
                    playerAttackable.setActive(False)

                    messaging.add(
                        type = MessageType.EntityDying,
                        groupId = playerGroupId.getId(),
                        data = {}
                    )
                    messaging.add(
                        type = MessageType.Gameover,
                        data = {}
                    )

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
            knockback = msg.data['knockback']
            isPlayer = self.world.has_component(entity, Player)

            # enemy can attack player, and vice-versa
            if not byPlayer ^ isPlayer:
                continue

            # change health
            meAttackable.adjustHealth(-1 * damage)

            # gfx: show floating damage numbers
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

            # gfx: emit on-hit particles
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

            # no stun, knockdown, knockback, or new color if there is no health left
            # (animations may overwrite each other)
            if meAttackable.getHealth() <= 0.0:
                return

            # gfx: set texture color
            healthPercentage = meAttackable.getHealthPercentage()
            if healthPercentage > 0.5:
                meRenderable.texture.setOverwriteColorFor(
                    0.1, ColorPalette.getColorByColor(Color.yellow))
            else:
                meRenderable.texture.setOverwriteColorFor(
                    0.1, ColorPalette.getColorByColor(Color.red))

            # handle: stun
            if meAttackable.isStunnable():
                stunTime = meAttackable.stunTime
                meAttackable.stunTimer.setTimer(timerValue=stunTime)
                meAttackable.stunTimer.start()
                meAttackable.isStunned = True
                meAttackable.addStun(stunTime=stunTime)

                # handle: knockdown
                if random.random() < meAttackable.knockdownChance:
                    messaging.add(
                        type=MessageType.EntityKnockdown,
                        data={},
                        groupId = meGroupId.getId(),
                    )
                else:
                    messaging.add(
                        type=MessageType.EntityStun,
                        data={
                            'timerValue': stunTime,
                        },
                        groupId = meGroupId.getId(),
                    )

                # no additional effects
                return

            # handle: knockback
            if knockback and random.random() < meAttackable.knockbackChance:
                if direction is Direction.left:
                    x = -2
                else:
                    x = 2

                directMessaging.add(
                    groupId = meGroupId.getId(),
                    type = DirectMessageType.moveEnemy,
                    data = {
                        'x': x,
                        'y': 0,
                        'dontChangeDirection': True,
                        'updateTexture': False,
                        'force': True,
                    },
                )

                # no additional effects
                return
