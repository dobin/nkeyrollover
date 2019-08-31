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

import system.renderable
import system.gamelogic.attackable 
import system.gamelogic.tenemy 
import system.gamelogic.tplayer

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

        self.damage = {
            WeaponType.hit: 50, 
            WeaponType.hitSquare: 50,
            WeaponType.hitLine: 50,
            WeaponType.jumpKick: 50
        }


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


    def attack(self):
        if not self.cooldownTimer.timeIsUp():
            RecordHolder.recordPlayerAttackCooldown(self.weaponType, time=self.cooldownTimer.getTimeLeft())
            return
        self.cooldownTimer.reset() # activate cooldown

        self.renderable.setActive(True)
        self.durationTimer.reset() # will setActive(false) when time is up

        if self.weaponType is WeaponType.hit:
            self.renderable.texture.changeAnimation(PhenomenaType.hit, self.renderable.parent.direction)
            hitLocations = self.renderable.texture.getTextureHitCoordinates()
        elif self.weaponType is WeaponType.hitSquare:
            self.renderable.texture.changeAnimation(PhenomenaType.hitSquare, self.renderable.parent.direction)
            hitLocations = self.renderable.texture.getTextureHitCoordinates()        
        elif self.weaponType is WeaponType.hitLine: 
            self.renderable.texture.changeAnimation(PhenomenaType.hitLine, self.renderable.parent.direction)
            hitLocations = self.renderable.texture.getTextureHitCoordinates()
        elif self.weaponType is WeaponType.jumpKick: 
            self.renderable.texture.changeAnimation(PhenomenaType.hit, self.renderable.parent.direction)
            hitLocations = []
        
        messageType = None
        if self.isPlayer:
            messageType = MessageType.PlayerAttack
        else: 
            messageType = MessageType.EnemyAttack

        messaging.add(
            type=messageType, 
            data= {
                'hitLocations': hitLocations,
                'damage': self.damage[ self.weaponType ]
            }
        )




    def advance(self, deltaTime :float):
        self.cooldownTimer.advance(deltaTime)
        self.durationTimer.advance(deltaTime)

        if self.durationTimer.isActive() and self.durationTimer.timeIsUp():
            self.renderable.setActive(False)

    def getWeaponStr(self): 
        return self.selectedWeaponKey



