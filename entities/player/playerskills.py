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

from system.gamelogic.attackable import Attackable
from system.gamelogic.tenemy import tEnemy
from system.gamelogic.tplayer import tPlayer
from system.renderable import Renderable

logger = logging.getLogger(__name__)


class PlayerSkills(object): 
    def __init__(self, player): 
        self.player = player
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


    def doSkillType(self, weaponType :WeaponType): 
        damage = 0
        if weaponType is WeaponType.explosion: 
            damage = self.skillExplosion()
        elif weaponType is WeaponType.laser:
            damage = self.skillLaser()
        elif weaponType is WeaponType.cleave:
            damage = self.skillCleave()
        elif weaponType is WeaponType.heal:
            damage = self.skillHeal()
        elif weaponType is WeaponType.switchside: 
            damage = self.skillSwitchSide()
        else: 
            logger.error("Unknown skill {}".format(weaponType))            

        RecordHolder.recordAttack(
            weaponType=weaponType, damage=damage, name=self.player.name, 
            characterType=self.player.entityType)


    def doSkill(self, key): 
        weaponType = None
        isCooldown = False

        if key == 'c': 
            self.player.speechTexture.changeAnimation('hoi')
            #self.player.actionCtrl.changeTo(
            #    CharacterAnimationType.shrugging, 
            #    self.player.direction)

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


    def skillHeal(self): 
        self.player.characterStatus.heal(100)
        return 0


    def skillSwitchSide(self): 
        screenCoordinates = self.player.viewport.getScreenCoords(self.player.coordinates)

        if screenCoordinates.x < (Config.columns / 2):
            diff = 80 - 2 * screenCoordinates.x
            self.player.coordinates.x += diff
        else: 
            diff = Config.areaMoveable['maxx'] - 2 * (Config.areaMoveable['maxx'] - screenCoordinates.x)
            self.player.coordinates.x -= diff
        return 0


    def skillExplosion(self): 
        locCenter = self.player.getLocationCenter()
        self.player.world.particleEmiter.emit(
            locCenter, 
            ParticleEffectType.explosion)
        hitLocations = Utility.getBorder(locCenter, distance=4, thicc=2)

        damage = self.hitCollisionDetection(hitLocations, weaponType=WeaponType.explosion)
        self.player.announce(damage=damage, particleEffectType=ParticleEffectType.explosion)
        return damage


    def skillLaser(self): 
        hitLocations = self.player.world.particleEmiter.emit(
            self.player.characterAttack.getLocation(), 
            ParticleEffectType.laser, 
            direction=self.player.direction)

        damage = self.hitCollisionDetection(hitLocations, weaponType=WeaponType.laser)
        self.player.announce(damage=damage, particleEffectType=ParticleEffectType.laser)
        return damage


    def skillCleave(self): 
        hitLocations = self.player.world.particleEmiter.emit(
            self.player.characterAttack.getLocation(), 
            ParticleEffectType.cleave, 
            direction=self.player.direction)

        damage = self.hitCollisionDetection(hitLocations, weaponType=WeaponType.cleave)
        self.player.announce(damage=damage, particleEffectType=ParticleEffectType.cleave)
        return damage


    def hitCollisionDetection(self, hitLocations, weaponType):
        damageSum = 0

        for ent, (renderable, attackable, enemy) in self.player.world.esperWorld.get_components(Renderable, Attackable, tEnemy):
            if renderable.isHitBy(hitLocations):
                damage = self.player.characterStatus.getDamage(weaponType=weaponType)
                attackable.handleHit(damage)
                renderable.r.setOverwriteColorFor( 
                    1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))
                damageSum += damage

        return damageSum


    def advance(self, dt):
        for _, timer in self.cooldownTimers.items():
            timer.advance(dt)
