import logging

from system.graphics.particleeffecttype import ParticleEffectType
from utilities.timer import Timer
import system.gamelogic.attackable
import system.graphics.renderable
import system.groupid
from messaging import messaging, MessageType
from directmessaging import directMessaging, DirectMessageType
from common.direction import Direction
from game.offenseloader.fileoffenseloader import fileOffenseLoader
from game.offenseloader.skilltype import SkillType

logger = logging.getLogger(__name__)


class OffensiveSkill(object):
    def __init__(self, esperData, viewport):
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
        self.data = {
            SkillType.port: {
                'distance': 20,
            }
        }


    def doSkillType(self, skillType :SkillType):
        if skillType is SkillType.explosion:
            self.skillExplosion()
        elif skillType is SkillType.laser:
            self.skillLaser()
        elif skillType is SkillType.cleave:
            self.skillCleave()
        elif skillType is SkillType.heal:
            self.skillHeal()
        elif skillType is SkillType.port:
            self.skillPort()
        else:
            logger.error("Unknown skill {}".format(skillType))


    def doSkill(self, key):
        skillType = None

        if key == 'c':
            self.skillSay('hoi')

        if key == 'f':
            skillType = SkillType.heal
            if self.isRdy(key):
                self.doSkillType(skillType)
                self.cooldownTimers[key].reset()

        if key == 'g':
            skillType = SkillType.port
            if self.isRdy(key):
                self.doSkillType(skillType)
                self.cooldownTimers[key].reset()

        if key == 'q':
            skillType = SkillType.cleave
            if self.isRdy(key):
                self.doSkillType(skillType)
                self.cooldownTimers[key].reset()

        if key == 'w':
            skillType = SkillType.laser
            if self.isRdy(key):
                self.doSkillType(skillType)
                self.cooldownTimers[key].reset()

        if key == 'e':
            skillType = SkillType.port
            if self.isRdy(key):
                self.doSkillType(skillType)
                self.cooldownTimers[key].reset()

        if key == 'r':
            skillType = SkillType.explosion
            if self.isRdy(key):
                self.doSkillType(skillType)
                self.cooldownTimers[key].reset()


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

        # self.player.actionCtrl.changeTo(
        #    CharacterAnimationType.shrugging,
        #    self.player.direction)


    def skillHeal(self):
        meAttackable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.gamelogic.attackable.Attackable)
        meAttackable.adjustHealth(50)


    def skillPort(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.graphics.renderable.Renderable)
        meGroupId = self.esperData.world.component_for_entity(
            self.esperData.entity, system.groupid.GroupId)

        moveX = 0
        if meRenderable.direction is Direction.left:
            moveX = -self.data[SkillType.port]['distance']
        if meRenderable.direction is Direction.right:
            moveX = self.data[SkillType.port]['distance']

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
        damage = fileOffenseLoader.skillManager.getSkillData(SkillType.explosion).damage
        particleEffectType = fileOffenseLoader.skillManager.getSkillData(SkillType.explosion).particleEffectType
        messaging.add(
            type=MessageType.EmitParticleEffect,
            data= {
                'location': locCenter,
                'effectType': particleEffectType,
                'damage': damage,
                'byPlayer': True,
                'direction': Direction.none,
            }
        )


    def skillLaser(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.graphics.renderable.Renderable)

        locCenter = meRenderable.getLocationCenter()
        damage = fileOffenseLoader.skillManager.getSkillData(SkillType.laser).damage
        particleEffectType = fileOffenseLoader.skillManager.getSkillData(SkillType.laser).particleEffectType
        messaging.add(
            type=MessageType.EmitParticleEffect,
            data= {
                'location': locCenter,
                'effectType': particleEffectType,
                'damage': damage,
                'byPlayer': True,
                'direction': meRenderable.direction,
            }
        )


    def skillCleave(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.graphics.renderable.Renderable)

        locCenter = meRenderable.getLocationCenter()
        damage = fileOffenseLoader.skillManager.getSkillData(SkillType.cleave).damage
        particleEffectType = fileOffenseLoader.skillManager.getSkillData(SkillType.cleave).particleEffectType
        messaging.add(
            type=MessageType.EmitParticleEffect,
            data= {
                'location': locCenter,
                'effectType': particleEffectType,
                'damage': damage,
                'byPlayer': True,
                'direction': meRenderable.direction,
            }
        )


    def advance(self, dt):
        for _, timer in self.cooldownTimers.items():
            timer.advance(dt)
