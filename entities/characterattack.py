from enum import Enum 
import logging

from utilities.timer import Timer
from sprite.phenomenasprite import PhenomenaSprite
from texture.phenomenatype import PhenomenaType
from config import Config
from .entity import Entity
from .entitytype import EntityType
from .character import Character
from .direction import Direction
from .character import Character
from .weapontype import WeaponType

logger = logging.getLogger(__name__)



class CharacterAttack(Entity): 
    def __init__(self, win, parentCharacter, isPlayer):
        # note that ParentCharacter(Character) is also an Entity, as required by Entity
        super(CharacterAttack, self).__init__(win=win, parentEntity=parentCharacter, entityType=EntityType.weapon)

        if not isinstance(parentCharacter, Character):
            raise ValueError("Character: Tried to use non-Character class as parent: " + str(parentCharacter))
        else: 
            self.parentCharacter = parentCharacter

        self.isPlayer = isPlayer
        self.sprite = PhenomenaSprite(phenomenaType=PhenomenaType.hit, parentEntity=self)

        # the duration of the hitting animation
        self.durationTimer.setTimer( self.sprite.getAnimationTime() )
        self.durationTimer.reset()

        # cooldown. 0.2 is actually lower than whats possible, even with 100fps
        self.cooldownTimer = Timer(0.2, instant=True)

        # for drawing the hit, and see if the char is "hitting"
        self.isActive = False

        self.weaponType = WeaponType.hit
        

    def switchWeapon(self, weaponType):
        logging.info("Switch to weaopn: " + str(weaponType))
        self.weaponType = weaponType

   
    def attackWeaponHit(self):
        if self.parentEntity.direction is Direction.right: 
            self.x = 3
            self.y = 1
        else: 
            self.x = -1
            self.y = 1
    
        self.sprite.changeTexture(PhenomenaType.hit, self.parentEntity.direction)
        self.hitCollisionDetection( [ self.getLocation()] )


    def attackWeaponHitSquare(self):
        if self.parentEntity.direction is Direction.right: 
            self.x = 3
            self.y = 0
        else: 
            self.x = -2
            self.y = 0

        self.sprite.changeTexture(PhenomenaType.hitSquare, self.parentEntity.direction)
        hitLocations = []
        hitLocationsBase = self.getLocation()
        
        hl2 = { 
            'x': hitLocationsBase['x'] + 1,
            'y': hitLocationsBase['y'],
        }
        hl3 = { 
            'x': hitLocationsBase['x'],
            'y': hitLocationsBase['y'] + 1,
        }
        hl4 = { 
            'x': hitLocationsBase['x'] + 1,
            'y': hitLocationsBase['y'] + 1,
        }

        hitLocations.append(hitLocationsBase)
        hitLocations.append(hl2)
        hitLocations.append(hl3)
        hitLocations.append(hl4)

        self.hitCollisionDetection( hitLocations )


    def attackWeaponHitLine(self): 
        if self.parentEntity.direction is Direction.right: 
            self.x = 3
            self.y = 1
        else: 
            self.x = -1
            self.y = 1

        self.sprite.changeTexture(PhenomenaType.hitLine, self.parentEntity.direction)
        hitLocations = []
        hitLocationsBase = self.getLocation()
        
        hl2 = { 
            'x': hitLocationsBase['x'] + 1,
            'y': hitLocationsBase['y'],
        }
        hl3 = { 
            'x': hitLocationsBase['x'] + 2,
            'y': hitLocationsBase['y'],
        }
        hl4 = { 
            'x': hitLocationsBase['x'] + 3,
            'y': hitLocationsBase['y'],
        }

        hitLocations.append(hitLocationsBase)
        hitLocations.append(hl2)
        hitLocations.append(hl3)
        hitLocations.append(hl4)

        self.hitCollisionDetection( hitLocations )


    def attackWeaponJumpKick(self): 
        self.sprite.changeTexture(PhenomenaType.hit, self.parentEntity.direction)


    def attack(self):
        if not self.cooldownTimer.timeIsUp():
            logging.debug("Hitting on cooldown")
            return
        self.cooldownTimer.reset() # activate cooldown

        self.isActive = True
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
                    enemy.gmHandleHit( self.parentCharacter.characterStatus.getDamage() )
        else: 
            for hitLocation in hitLocations:
                hittedPlayer = self.parentCharacter.world.director.getPlayersHit(hitLocation)
                for player in hittedPlayer: 
                    player.gmHandleHit( self.parentCharacter.characterStatus.getDamage() )



    # we overwrite getLocation for now, as we need to know
    # the direction parent is facing
    #def getLocation(self): 
    #    loc = self.parentEntity.getLocation()
    #
    #    if self.parentEntity.direction is Direction.right: 
    #        loc['x'] += 3
    #        loc['y'] += 1
    #    else: 
    #        loc['x'] -= 1
    #        loc['y'] += 1
    #
    #    return loc

    
    def advance(self, deltaTime):
        super(CharacterAttack, self).advance(deltaTime)
        self.cooldownTimer.advance(deltaTime)