from enum import Enum 
import logging

from sprite.coordinates import Coordinates
from utilities.timer import Timer
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from config import Config
from .entity import Entity
from .entitytype import EntityType
from .character import Character
from sprite.direction import Direction
from .character import Character
from .weapontype import WeaponType
from world.viewport import Viewport

logger = logging.getLogger(__name__)


class CharacterAttack(Entity): 
    def __init__(self, viewport, parentCharacter :Character, isPlayer :bool):
        super(CharacterAttack, self).__init__(viewport=viewport, parentSprite=parentCharacter, entityType=EntityType.weapon)

        self.isPlayer = isPlayer
        self.texture = PhenomenaTexture(phenomenaType=PhenomenaType.hit, parentSprite=self)
        self.parentCharacter = parentCharacter

        # the duration of the hitting animation
        self.durationTimer.setTimer( self.texture.getAnimationTime() )
        self.durationTimer.reset()

        # cooldown. 0.2 is actually lower than whats possible, even with 100fps
        self.cooldownTimer = Timer(0.2, instant=True)

        # for drawing the hit, and see if the char is "hitting"
        self.setActive(False)

        self.weaponType = WeaponType.hit
        self.selectedWeaponKey = '1'
        

    def switchWeaponByKey(self, key):
        self.selectedWeaponKey = key
        if key == '1':
            self.switchWeapon(WeaponType.hit)

        if key == '2':
            self.switchWeapon(WeaponType.hitSquare)

        if key == '3':
            self.switchWeapon(WeaponType.hitLine)

        if key == '4':
            self.switchWeapon(WeaponType.jumpKick)


    def switchWeapon(self, weaponType):
        logger.info("Switch to weaopn: " + str(weaponType))
        self.weaponType = weaponType

   
    def attackWeaponHit(self):
        self.texture.changeAnimation(PhenomenaType.hit, self.parentSprite.direction)
        self.hitCollisionDetection( [ self.getLocation()] )


    def getLocation(self): 
        baselocation = super(CharacterAttack, self).getLocation()

        if self.weaponType is WeaponType.hit: 
            if self.parentSprite.direction is Direction.right: 
                baselocation.x += 3
                baselocation.y += 1
            else: 
                baselocation.x -= 1
                baselocation.y += 1
        elif self.weaponType is WeaponType.hitSquare: 
            if self.parentSprite.direction is Direction.right: 
                baselocation.x += 3
                #baselocation.y = 0
            else: 
                baselocation.x -= 2
                #baselocation.y = 0
        elif self.weaponType is WeaponType.hitLine: 
            if self.parentSprite.direction is Direction.right: 
                baselocation.x += 3
                baselocation.y += 1
            else: 
                baselocation.x -= 4
                baselocation.y += 1

        return baselocation
        

    def attackWeaponHitSquare(self):
        self.texture.changeAnimation(PhenomenaType.hitSquare, self.parentSprite.direction)
        hitLocations = []
        hitLocationsBase = self.getLocation()
        
        hl2 = Coordinates( 
            x = hitLocationsBase.x + 1,
            y = hitLocationsBase.y,
        )
        hl3 = Coordinates( 
            x = hitLocationsBase.x,
            y = hitLocationsBase.y + 1,
        )
        hl4 = Coordinates( 
            x = hitLocationsBase.x + 1,
            y = hitLocationsBase.y + 1,
        )

        hitLocations.append(hitLocationsBase)
        hitLocations.append(hl2)
        hitLocations.append(hl3)
        hitLocations.append(hl4)

        self.hitCollisionDetection( hitLocations )


    def attackWeaponHitLine(self): 
        self.texture.changeAnimation(PhenomenaType.hitLine, self.parentSprite.direction)
        hitLocations = []
        hitLocationsBase = self.getLocation()
        
        hl2 = Coordinates( 
            x = hitLocationsBase.x + 1,
            y = hitLocationsBase.y,
        )
        hl3 = Coordinates( 
            x = hitLocationsBase.x + 2,
            y = hitLocationsBase.y,
        )
        hl4 = Coordinates( 
            x = hitLocationsBase.x + 3,
            y = hitLocationsBase.y,
        )

        hitLocations.append(hitLocationsBase)
        hitLocations.append(hl2)
        hitLocations.append(hl3)
        hitLocations.append(hl4)

        self.hitCollisionDetection( hitLocations )


    def attackWeaponJumpKick(self): 
        self.texture.changeAnimation(PhenomenaType.hit, self.parentSprite.direction)


    def attack(self):
        if not self.cooldownTimer.timeIsUp():
            logger.debug("Hitting on cooldown")
            return
        self.cooldownTimer.reset() # activate cooldown

        self.setActive(True)
        self.durationTimer.reset() # entity will setActive(false) when time is up

        if self.weaponType is WeaponType.hit:
            self.attackWeaponHit()
        elif self.weaponType is WeaponType.hitSquare:
            self.attackWeaponHitSquare()
        elif self.weaponType is WeaponType.hitLine: 
            self.attackWeaponHitLine()
        elif self.weaponType is WeaponType.jumpKick: 
            self.attackWeaponJumpKick()


    def hitCollisionDetection(self, hitLocations):
        if self.isPlayer:
            for hitLocation in hitLocations:
                hittedEnemies = self.parentCharacter.world.director.getEnemiesHit(hitLocation)
                for enemy in hittedEnemies:
                    enemy.gmHandleHit( 
                        self.parentCharacter.characterStatus.getDamage(weaponType=self.weaponType) )
                    self.parentCharacter.gmHandleEnemyHit( 
                        self.parentCharacter.characterStatus.getDamage(weaponType=self.weaponType) ) 
        else: 
            for hitLocation in hitLocations:
                hittedPlayer = self.parentCharacter.world.director.getPlayersHit(hitLocation)
                for player in hittedPlayer: 
                    player.gmHandleHit( 
                        self.parentCharacter.characterStatus.getDamage(weaponType=self.weaponType) )
                    self.parentCharacter.gmHandleEnemyHit( 
                        self.parentCharacter.characterStatus.getDamage(weaponType=self.weaponType) ) 


    def advance(self, deltaTime):
        super(CharacterAttack, self).advance(deltaTime)
        self.cooldownTimer.advance(deltaTime)


    def getWeaponStr(self): 
        return self.selectedWeaponKey