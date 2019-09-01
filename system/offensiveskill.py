import logging 

from utilities.recordholder import RecordHolder
from config import Config
from world.particleeffecttype import ParticleEffectType
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from utilities.utilities import Utility
from entities.weapontype import WeaponType
from utilities.colorpalette import ColorPalette
from utilities.color import Color

import system.gamelogic.attackable 
import system.renderable
import system.graphics.speechbubble

from messaging import messaging, Messaging, Message, MessageType


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
            WeaponType.switchside: 0,
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
        elif weaponType is WeaponType.switchside: 
            self.skillSwitchSide()
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
            weaponType = WeaponType.switchside
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
            weaponType = WeaponType.switchside
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
        for ent, (renderable, speechBubble) in self.esperData.world.get_components(
            system.renderable.Renderable, system.graphics.speechbubble.SpeechBubble
        ):
            speechBubble.changeText(text)
            #self.player.actionCtrl.changeTo(
            #    CharacterAnimationType.shrugging, 
            #    self.player.direction)


    def skillHeal(self): 
        meAttackable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.gamelogic.attackable.Attackable)
        meAttackable.heal(50)


    def skillSwitchSide(self): 
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.renderable.Renderable)

        screenCoordinates = self.viewport.getScreenCoords(
            meRenderable.getLocation())
        
        if screenCoordinates.x < (Config.columns / 2):
            diff = 80 - 2 * screenCoordinates.x
            meRenderable.coordinates.x += diff
        else: 
            diff = Config.areaMoveable['maxx'] - 2 * (Config.areaMoveable['maxx'] - screenCoordinates.x)
            meRenderable.coordinates.x -= diff


    def skillExplosion(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.renderable.Renderable)

        locCenter = meRenderable.getLocationCenter()
        self.particleEmiter.emit(
            locCenter, 
            ParticleEffectType.explosion)
        hitLocations = Utility.getBorder(locCenter, distance=4, thicc=2)

        messaging.add(
            type=MessageType.PlayerAttack, 
            data= {
                'hitLocations': hitLocations,
                'damage': self.damage[ WeaponType.explosion ]
            }
        )

        #self.player.announce(damage=damage, particleEffectType=ParticleEffectType.explosion)


    def skillLaser(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.renderable.Renderable)

        hitLocations = self.particleEmiter.emit(
            meRenderable.getLocation(), 
            ParticleEffectType.laser, 
            direction=meRenderable.direction)

        messaging.add(
            type=MessageType.PlayerAttack, 
            data= {
                'hitLocations': hitLocations,
                'damage': self.damage[ WeaponType.laser ]
            }
        )
        #self.player.announce(damage=damage, particleEffectType=ParticleEffectType.laser)


    def skillCleave(self):
        meRenderable = self.esperData.world.component_for_entity(
            self.esperData.entity, system.renderable.Renderable)        

        hitLocations = self.particleEmiter.emit(
            meRenderable.getLocation(), 
            ParticleEffectType.cleave, 
            direction=meRenderable.direction)

        messaging.add(
            type=MessageType.PlayerAttack, 
            data= {
                'hitLocations': hitLocations,
                'damage': self.damage[ WeaponType.cleave ]
            }
        )

        #self.player.announce(damage=damage, particleEffectType=ParticleEffectType.cleave)


    def advance(self, dt):
        for _, timer in self.cooldownTimers.items():
            timer.advance(dt)
