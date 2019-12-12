import esper
import logging
import random

from system.graphics.destructable import Destructable
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

logger = logging.getLogger("AttackableProcessor")


class AttackableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        healthUpdated = self.checkReceiveDamage()
        if healthUpdated:
            self.checkHealth()
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

        # environment
        for ent, (destructable, meAtk, meGroupId, meRend) in self.world.get_components(
            Destructable, Attackable, GroupId, Renderable
        ):
            if meAtk.getHealth() <= 0:
                meRend.texture.setActive(False)
            else:
                frameCount = meRend.texture.animation.frameCount - 1
                d = meAtk.getHealth() / (meAtk.initialHealth / frameCount)
                animationIndex = frameCount - int(d)

                if animationIndex != meRend.texture.frameIndex:
                    meRend.texture.advanceStep()


    def checkReceiveDamage(self):
        healthUpdated = False

        for msg in directMessaging.getByType(DirectMessageType.receiveDamage):
            entity = EntityFinder.findAttackableByGroupId(self.world, msg.groupId)
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
            stun = msg.data['stun']
            isPlayer = self.world.has_component(entity, Player)

            # enemy can attack player, and vice-versa
            if not byPlayer ^ isPlayer:
                continue

            if damage == 0:
                continue

            # change health
            meAttackable.adjustHealth(-1 * damage)
            healthUpdated = True
            logger.info("{} got {} damage, new health: {}".format(
                meRenderable, damage, meAttackable.getHealth()))

            # gfx: show floating damage numbers
            if Config.showEnemyDamageNumbers:
                messaging.add(
                    type=MessageType.EmitMirageParticleEffect,
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
                        type=MessageType.EmitMirageParticleEffect,
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
                continue

            # gfx: set texture color
            healthPercentage = meAttackable.getHealthPercentage()
            if healthPercentage > 0.5:
                meRenderable.texture.setOverwriteColorFor(
                    Config.overwriteColorTime,
                    ColorPalette.getColorByColor(Color.yellow))
            else:
                meRenderable.texture.setOverwriteColorFor(
                    Config.overwriteColorTime,
                    ColorPalette.getColorByColor(Color.red))

            # handle: stun
            if stun and meAttackable.isStunnable():
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
                continue

            # handle: knockback
            if knockback and random.random() < meAttackable.knockbackChance:
                if direction is Direction.left:
                    x = -2
                else:
                    x = 2

                if isPlayer:
                    directMessaging.add(
                        groupId = meGroupId.getId(),
                        type = DirectMessageType.movePlayer,
                        data = {
                            'x': x,
                            'y': 0,
                            'dontChangeDirection': True,
                            'whenMoved': "showOnKnockback",
                        },
                    )
                else:
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
                continue

        return healthUpdated
