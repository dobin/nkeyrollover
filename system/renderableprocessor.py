import esper
import copy
import logging
from typing import List

from sprite.coordinates import Coordinates
from entities.character import Character
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.timer import Timer
from utilities.color import Color
from sprite.direction import Direction
from texture.character.characteranimationtype import CharacterAnimationType
from messaging import messaging, Messaging, Message, MessageType
from config import Config

import system.gamelogic.attackable
import system.gamelogic.enemy
import system.gamelogic.player
import system.renderable

logger = logging.getLogger(__name__)


class RenderableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

        # list of HEIGHT lists
        self.renderOrder = [[] for i in range(Config.rows + 3)]


    def process(self, dt):
        self.collisionDetection()
        self.advance(dt)
        self.render()


    def advance(self, deltaTime):
        for ent, rend in self.world.get_component(system.renderable.Renderable):
            rend.advance(deltaTime)


    def collisionDetection(self): 
        damageSum = 0
        for message in messaging.get():
            if message.type is MessageType.PlayerAttack: 
                hitLocations = message.data['hitLocations']
                damage = message.data['damage']

                for ent, (renderable, attackable, enemy) in self.world.get_components(
                    system.renderable.Renderable, system.gamelogic.attackable.Attackable, system.gamelogic.enemy.Enemy
                ):
                    if renderable.isHitBy(hitLocations):
                        attackable.handleHit(damage)
                        renderable.setOverwriteColorFor( 
                            1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))
                        damageSum += damage

            if message.type is MessageType.EnemyAttack:
                hitLocations = message.data['hitLocations']
                damage = message.data['damage']

                for ent, (renderable, attackable, player) in self.world.get_components(
                    system.renderable.Renderable, system.gamelogic.attackable.Attackable, system.gamelogic.player.Player
                ):
                    if renderable.isHitBy(hitLocations):
                        attackable.handleHit(damage)
                        renderable.setOverwriteColorFor( 
                            1.0 - 1.0/damage , ColorPalette.getColorByColor(Color.red))
                        damageSum += damage

        #RecordHolder.recordAttack(
        #    weaponType=self.weaponType, damage=damage, name=self.renderable.parent.name, 
        #    characterType=self.renderable.parent.entityType)
        

    def render(self):
        for l in self.renderOrder: 
            l.clear()
        
        # add all elements to draw in the correct Z order
        # which is by y coordinates
        for ent, rend in self.world.get_component(system.renderable.Renderable):
            if rend.isActive():
                #logging.info("REND: {} {} {}".format(rend, rend.z, rend.coordinates))
                loc = rend.getLocation()
                self.renderOrder[ loc.y + rend.z ].append(rend)
            
        for l in self.renderOrder:
            for rend in l:
                rend.draw()