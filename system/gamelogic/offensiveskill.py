import logging

from utilities.recordholder import RecordHolder
from world.particleeffecttype import ParticleEffectType
from utilities.timer import Timer
from utilities.utilities import Utility
from entities.weapontype import WeaponType
import system.gamelogic.attackable
import system.graphics.renderable
import system.groupid
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
from sprite.direction import Direction

logger = logging.getLogger(__name__)


class OffensiveSkill(object):
    def __init__(self, esperData, particleEmiter, viewport):
        self.particleEmiter = particleEmiter
        self.esperData = esperData
        self.viewport = viewport

        self.skillStatus = [
            'q', 'w', 'e', 'r', 'f', 'g'
        ]
        self.cooldownTimers = {
            'q': Timer(1.0, instant=True),
            'w': Timer(1.0, instant=True),
            'e': Timer(5.0, instant=True),
            'r': Timer(3.0, instant=True),

            'c': Timer(1.0, instant=True),
            'f': Timer(30.0, instant=True),
            'g': Timer(5.0, instant=True),
        }
        self.damage = {
            WeaponType.explosion: 100,
            WeaponType.laser: 100,
            WeaponType.cleave: 100,
            WeaponType.heal: 0,
            WeaponType.port: 0,
        }
        self.data = {
            WeaponType.port: {
                'distance': 20,
            }
        }


    def doSkillType(self, weaponType :WeaponType):
        if weaponType is WeaponType.explosion:
            self.skillExplosion()
        elif weaponType is WeaponType.laser:
            self.skillLaser()
        elif weaponType is WeaponType.cleave:
            self.skillCleave()
        elif weaponType is WeaponType.heal:
            self.skillHeal()
        elif weaponType is WeaponType.port:
            self.skillPort()
        else:
            logger.error("Unknown skill {}".format(weaponType))

        #RecordHolder.recordAttack(
        #    weaponType=weaponType, damage=damage, name=self.player.name,
        #    characterType=self.player.entityType)


    def doSkill(self, key):
        weaponType = None
        isCooldown = False

        if key == 'c':
            self.skillSay('hoi')

        if key == 'f':
            weaponType = WeaponType.heal
            if self.isRdy(key):
                self.doSkillType(weaponType)
                self.cooldownTimers[key].reset()
            else:
                isCooldown = True

        if key == 'g':
            weaponType = WeaponType.port
            if self.isRdy(key):
                self.doSkillType(weaponType)
                self.cooldownTimers[key].reset()
            else:
                isCooldown = True

        if key == 'q':
            weaponType = WeaponType.cleave
            if self.isRdy(key):
                self.doSkillType(weaponType)
                self.cooldownTimers[key].reset()
            else:
                isCooldown = True

        if key == 'w':
            weaponType = WeaponType.laser
            if self.isRdy(key):
                self.doSkillType(weaponType)
                self.cooldownTimers[key].reset()
            else:
                isCooldown = True

        if key == 'e':
            weaponType = WeaponType.port
            if self.isRdy(key):
                self.doSkillType(weaponType)
                self.cooldownTimers[key].reset()
            else:
                isCooldown = True

        if key == 'r':
            weaponType = WeaponType.explosion
            if self.isRdy(key):
                self.doSkillType(weaponType)
                self.cooldownTimers[key].reset()
            else:
                isCooldown = True

        if isCooldown:
            RecordHolder.recordPlayerAttackCooldown(
                weaponType, self.cooldownTimers[key].getTimeLeft())


    def isRdy(self, skill):
        return self.cooldownTimers[skill].timeIsUp()


    def skillSay(self, text):
        meGroupId = self.esperData.world.component_for_entity(
            self.esperData.entity, system.groupid.GroupId)

        directMessaging.add(
            groupId = meGroupId.getId(),
            type = DirectMessageType.activateSpeechBubble,
            data = {
                'text': 'hoi',
                'time': 0.5,
                'waitTime': 0,
            }
        )

        #self.player.actionCtrl.changeTo(
        #    CharacterAnimationType.shrugging,
        #    self.player.direction)


    def skillHeal(self):
        meAttackable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.gamelogic.attackable.Attackable)
        meAttackable.heal(50)


    def skillPort(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.graphics.renderable.Renderable)
        meGroupId = self.esperData.world.component_for_entity(
            self.esperData.entity, system.groupid.GroupId)

        moveX = 0
        if meRenderable.direction is Direction.left: 
            moveX = -self.data[WeaponType.port]['distance']
        if meRenderable.direction is Direction.right: 
            moveX = self.data[WeaponType.port]['distance']

        directMessaging.add(
            type = DirectMessageType.movePlayer,
            groupId = meGroupId.getId(),
            data = {
                'x': moveX,
                'y': 0,
            }
        )


    def skillExplosion(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.graphics.renderable.Renderable)

        locCenter = meRenderable.getLocationCenter()
        self.particleEmiter.emit(
            locCenter,
            ParticleEffectType.explosion)
        hitLocations = Utility.getBorder(locCenter, distance=4, thicc=2)

        messaging.add(
            type=MessageType.PlayerAttack,
            data= {
                'hitLocations': hitLocations,
                'damage': self.damage[WeaponType.explosion]
            }
        )
        #self.player.announce(damage=damage, particleEffectType=ParticleEffectType.explosion)


    def skillLaser(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.graphics.renderable.Renderable)

        hitLocations = self.particleEmiter.emit(
            meRenderable.getLocationCenter(),
            ParticleEffectType.laser,
            direction=meRenderable.direction)

        messaging.add(
            type=MessageType.PlayerAttack,
            data= {
                'hitLocations': hitLocations,
                'damage': self.damage[WeaponType.laser]
            }
        )
        #self.player.announce(damage=damage, particleEffectType=ParticleEffectType.laser)


    def skillCleave(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.graphics.renderable.Renderable)

        hitLocations = self.particleEmiter.emit(
            meRenderable.getLocationCenter(),
            ParticleEffectType.cleave,
            direction=meRenderable.direction)

        messaging.add(
            type=MessageType.PlayerAttack,
            data= {
                'hitLocations': hitLocations,
                'damage': self.damage[WeaponType.cleave]
            }
        )
        #self.player.announce(damage=damage, particleEffectType=ParticleEffectType.cleave)


    def advance(self, dt):
        for _, timer in self.cooldownTimers.items():
            timer.advance(dt)
