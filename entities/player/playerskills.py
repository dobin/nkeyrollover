from config import Config
from world.particleeffecttype import ParticleEffectType
from texture.character.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer
from utilities.utilities import Utility
from entities.weapontype import WeaponType

class PlayerSkills(object): 
    def __init__(self, player): 
        self.player = player
        self.skillStatus = [
            'q', 'w', 'e', 'r'
        ]
        self.cooldownTimers = {
            'q': Timer(1.0, instant=True),
            'w': Timer(1.0, instant=True),
            'e': Timer(5.0, instant=True),
            'r': Timer(3.0, instant=True),
        }


    def doSkill(self, key): 
        if key == 'c': 
            self.player.speechTexture.changeAnimation('hoi')
            self.player.actionCtrl.changeTo(
                CharacterAnimationType.shrugging, 
                self.player.direction)

        if key == 'q': 
            if self.isRdy(key): 
                self.skillCleave()
                self.cooldownTimers[key].reset()
        
        if key == 'w':
            if self.isRdy(key): 
                self.skillLaser()
                self.cooldownTimers[key].reset()

        if key == 'e':
            if self.isRdy(key): 
                self.skillSwitchSide()
                self.cooldownTimers[key].reset()

        if key == 'r':
            if self.isRdy(key): 
                self.skillExplosion()
                self.cooldownTimers[key].reset()


    def isRdy(self, skill):
        return self.cooldownTimers[skill].timeIsUp()


    def skillSwitchSide(self): 
        if self.player.coordinates.x < (Config.rows / 2):
            self.player.coordinates.x = Config.areaMoveable['maxx'] - self.player.coordinates.x
        else: 
            self.player.coordinates.x = (Config.areaMoveable['maxx'] - self.player.coordinates.x)


    def skillExplosion(self): 
        self.player.world.particleEmiter.emit(
            self.player.getLocationCenter(), 
            ParticleEffectType.explosion)

        locCenter = self.player.getLocationCenter()
        hitLocations = Utility.getBorder(locCenter)

        damage = self.hitCollisionDetection(hitLocations, weaponType=WeaponType.explosion)
        self.player.announce(damage=damage, particleEffectType=ParticleEffectType.explosion)


    def skillLaser(self): 
        hitLocations = self.player.world.particleEmiter.emit(
            self.player.characterAttack.getLocation(), 
            ParticleEffectType.laser, 
            direction=self.player.direction)

        damage = self.hitCollisionDetection(hitLocations, weaponType=WeaponType.laser)
        self.player.announce(damage=damage, particleEffectType=ParticleEffectType.laser)


    def skillCleave(self): 
        hitLocations = self.player.world.particleEmiter.emit(
            self.player.characterAttack.getLocation(), 
            ParticleEffectType.cleave, 
            direction=self.player.direction)

        damage = self.hitCollisionDetection(hitLocations, weaponType=WeaponType.cleave)
        self.player.announce(damage=damage, particleEffectType=ParticleEffectType.cleave)


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
