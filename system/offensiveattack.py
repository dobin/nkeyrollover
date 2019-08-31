import esper

from enum import Enum 
import logging

from utilities.recordholder import RecordHolder
from sprite.coordinates import Coordinates
from utilities.timer import Timer
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from config import Config
from entities.entity import Entity
from entities.entitytype import EntityType
from entities.character import Character
from sprite.direction import Direction
from entities.character import Character
from entities.weapontype import WeaponType
from world.viewport import Viewport
from typing import List
from utilities.colorpalette import ColorPalette
from utilities.color import Color

from system.renderable import Renderable
from system.gamelogic.attackable import Attackable
#from system.gamelogic.tenemy import tEnemy
#from system.gamelogic.tplayer import tPlayer

from messaging import messaging, Messaging, Message, MessageType


logger = logging.getLogger(__name__)


class OffensiveAttack():
    def __init__(self, isPlayer, renderable, world):
        self.isPlayer :bool = isPlayer
        self.renderable = renderable
        self.world = world

        self.durationTimer = Timer(0.0, active=False)

        # the duration of the hitting animation
        self.durationTimer.setTimer( renderable.texture.getAnimationTime() )
        self.durationTimer.reset()

        self.cooldownTimer :Timer =Timer(Config.playerAttacksCd, instant=True)

        self.weaponType :WeaponType = WeaponType.hit
        self.selectedWeaponKey :str = '1'


    def switchWeaponByKey(self, key :str):
        self.selectedWeaponKey = key
        if key == '1':
            self.switchWeapon(WeaponType.hit)

        if key == '2':
            self.switchWeapon(WeaponType.hitSquare)

        if key == '3':
            self.switchWeapon(WeaponType.hitLine)

        if key == '4':
            self.switchWeapon(WeaponType.jumpKick)


    def switchWeapon(self, weaponType :WeaponType):
        logger.info("Switch to weaopn: " + str(weaponType))
        self.weaponType = weaponType

        # TODO: This is ugly..
        self.renderable.texture.changeAnimation(self.weaponTypeToAnimationType(weaponType), self.renderable.parent.direction)
        coordinates = Coordinates( # for hit
            -1 * self.renderable.texture.width,
            1
        )
        self.renderable.setLocation(coordinates)

    def weaponTypeToAnimationType(self, weaponType):
        if self.weaponType is WeaponType.hit:
            return PhenomenaType.hit
        elif self.weaponType is WeaponType.hitSquare:
            return PhenomenaType.hitSquare
        elif self.weaponType is WeaponType.hitLine: 
            return PhenomenaType.hitLine
        elif self.weaponType is WeaponType.jumpKick: 
            return PhenomenaType.hit


    def __getLocation(self) -> Coordinates: 
        baselocation = self.renderable.parent.getLocation()

        xx = None
        if self.renderable.parent.direction is Direction.right:
            xx = 1
        else: 
            xx = -1

        # new 1-pt weapon location
        charHalfWidth = int(self.renderable.parent.texture.width / 2.0)
        charHalfHeight = int( float(self.renderable.parent.texture.height) / 2.0)
        baselocation.y += charHalfHeight
        if self.renderable.parent.direction is Direction.left: 
            baselocation.x -= 1
        else: 
            baselocation.x += self.renderable.parent.texture.width

        # adjust for weapon area
        if self.weaponType is WeaponType.hit:
            pass # all good

        elif self.weaponType is WeaponType.hitSquare: 
            baselocation.y -= 1 # move it up one notch

            if self.renderable.parent.direction is Direction.left:
                baselocation.x -= self.renderable.texture.width - 1

        elif self.weaponType is WeaponType.hitLine: 
            if self.renderable.parent.direction is Direction.left:
                baselocation.x -= self.renderable.texture.width - 1

        return baselocation


    def attackWeaponHit(self) -> int:
        self.renderable.texture.changeAnimation(PhenomenaType.hit, self.renderable.parent.direction)
        
        # take hit locations from texture
        hitLocations = self.renderable.texture.getTextureHitCoordinates()

        damage = self.hitCollisionDetection( hitLocations )
        return damage        


    def attackWeaponHitSquare(self) -> int:
        self.renderable.texture.changeAnimation(PhenomenaType.hitSquare, self.renderable.parent.direction)
        
        # take hit locations from texture
        hitLocations = self.renderable.texture.getTextureHitCoordinates()

        damage = self.hitCollisionDetection( hitLocations )
        return damage


    def attackWeaponHitLine(self) -> int: 
        self.renderable.texture.changeAnimation(PhenomenaType.hitLine, self.renderable.parent.direction)
        
        # take hit locations from texture
        hitLocations = self.renderable.texture.getTextureHitCoordinates()

        damage = self.hitCollisionDetection( hitLocations )
        return damage


    def attackWeaponJumpKick(self) -> int: 
        self.renderable.texture.changeAnimation(PhenomenaType.hit, self.renderable.parent.direction)
        return 0


    def attack(self):
        if not self.cooldownTimer.timeIsUp():
            RecordHolder.recordPlayerAttackCooldown(self.weaponType, time=self.cooldownTimer.getTimeLeft())
            return
        self.cooldownTimer.reset() # activate cooldown

        self.renderable.setActive(True)
        self.durationTimer.reset() # entity will setActive(false) when time is up

        damage = 0
        if self.weaponType is WeaponType.hit:
            damage = self.attackWeaponHit()
        elif self.weaponType is WeaponType.hitSquare:
            damage = self.attackWeaponHitSquare()
        elif self.weaponType is WeaponType.hitLine: 
            damage = self.attackWeaponHitLine()
        elif self.weaponType is WeaponType.jumpKick: 
            damage = self.attackWeaponJumpKick()

        #RecordHolder.recordAttack(
        #    weaponType=self.weaponType, damage=damage, name=self.renderable.parent.name, 
        #    characterType=self.renderable.parent.entityType)


    def hitCollisionDetection(self, hitLocations :List[Coordinates]) -> int:
        damageSum = 0
        if self.isPlayer:
            #for ent, (renderable, attackable, enemy) in self.world.esperWorld.get_components(Renderable, Attackable, tEnemy):
            for ent, (renderable, attackable) in self.world.esperWorld.get_components(Renderable, Attackable):
                if renderable.isHitBy(hitLocations):
                    #damage = enemy.characterStatus.getDamage(weaponType=self.weaponType)
                    damage = 10
                    attackable.handleHit(damage)
                    renderable.setOverwriteColorFor( 
                        1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))
                    damageSum += damage

        else:
            #for ent, (renderable, attackable, player) in self.world.esperWorld.get_components(Renderable, Attackable, tPlayer):
            for ent, (renderable, attackable) in self.world.esperWorld.get_components(Renderable, Attackable):
                if renderable.isHitBy(hitLocations):
                    #damage = player.characterStatus.getDamage(weaponType=self.weaponType)
                    damage = 10
                    renderable.setOverwriteColorFor( 
                        1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))
                    damageSum += damage

        return damageSum


    def advance(self, deltaTime :float):
        self.cooldownTimer.advance(deltaTime)
        self.durationTimer.advance(deltaTime)

        if self.durationTimer.isActive() and self.durationTimer.timeIsUp():
            self.renderable.setActive(False)

    def getWeaponStr(self): 
        return self.selectedWeaponKey



