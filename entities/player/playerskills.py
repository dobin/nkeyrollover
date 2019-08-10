import logging 

from utilities.recordholder import RecordHolder
from config import Config
from world.particleeffecttype import ParticleEffectType
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from utilities.utilities import Utility
from entities.weapontype import WeaponType

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

        RecordHolder.recordPlayerAttack(weaponType=weaponType, damage=damage)


    def doSkill(self, key): 
        if key == 'c': 
            self.player.speechTexture.changeAnimation('hoi')
            #self.player.actionCtrl.changeTo(
            #    CharacterAnimationType.shrugging, 
            #    self.player.direction)

        if key == 'f':
            if self.isRdy(key): 
                # self.skillHeal()
                self.doSkillType(WeaponType.heal)
                self.cooldownTimers[key].reset()

        if key == 'g':
            if self.isRdy(key): 
                #self.skillSwitchSide()
                self.doSkillType(WeaponType.switchside)
                self.cooldownTimers[key].reset()

        if key == 'q': 
            if self.isRdy(key): 
                #self.skillCleave()
                self.doSkillType(WeaponType.cleave)
                self.cooldownTimers[key].reset()
        
        if key == 'w':
            if self.isRdy(key): 
                #self.skillLaser()
                self.doSkillType(WeaponType.laser)
                self.cooldownTimers[key].reset()

        if key == 'e':
            if self.isRdy(key): 
                #self.skillSwitchSide()
                self.doSkillType(WeaponType.switchside)
                self.cooldownTimers[key].reset()

        if key == 'r':
            if self.isRdy(key): 
                #self.skillExplosion()
                self.doSkillType(WeaponType.explosion)
                self.cooldownTimers[key].reset()


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
        self.player.world.particleEmiter.emit(
            self.player.getLocationCenter(), 
            ParticleEffectType.explosion)

        locCenter = self.player.getLocationCenter()
        hitLocations = Utility.getBorder(locCenter)

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
        damage = 0
        for hitLocation in hitLocations:
            hittedEnemies = self.player.world.director.getEnemiesHit(hitLocation)
            for enemy in hittedEnemies: 
                enemy.gmHandleHit( 
                    self.player.characterStatus.getDamage(weaponType=weaponType) )
                self.player.gmHandleEnemyHit( 
                    self.player.characterStatus.getDamage(weaponType=weaponType), 
                    isAttack=False )
                damage += self.player.characterStatus.getDamage(weaponType=weaponType)

        return damage


    def advance(self, dt):
        for _, timer in self.cooldownTimers.items():
            timer.advance(dt)
