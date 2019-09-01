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
import system.groupid

from directmessaging import directMessaging, DirectMessage, DirectMessageType


logger = logging.getLogger(__name__)


class RenderableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()

        # list of HEIGHT lists
        # used to add renderable objects in the right Z order for render()
        self.renderOrder = [[] for i in range(Config.rows + 3)]


    def process(self, dt):
        self.move()
        self.speechBubbleActivator()

        self.collisionDetection()
        self.advance(dt)
        self.render()


    def findEnemyByGroupId(self, id):
        for ent, (groupId, enemy, renderable) in self.world.get_components(
            system.groupid.GroupId, 
            system.gamelogic.enemy.Enemy, 
            system.renderable.Renderable
        ):
            if groupId.getId() == id:
                return renderable


    def move(self): 
        # findplayer
        for ent, (groupId, player, renderable) in self.world.get_components(
            system.groupid.GroupId, 
            system.gamelogic.player.Player, 
            system.renderable.Renderable
        ):
            msg = directMessaging.get(
                messageType = DirectMessageType.movePlayer
            )
            while msg is not None:
                self.moveRenderable(renderable, msg.data['x'], msg.data['y'])

                msg = directMessaging.get(
                    messageType = DirectMessageType.activateSpeechBubble
                )  

        # enemies
        msg = directMessaging.get(
            messageType = DirectMessageType.moveEnemy
        )
        while msg is not None:
            renderable = self.findEnemyByGroupId(msg.groupId)
            self.moveRenderable(renderable, msg.data['x'], msg.data['y'], msg.data['dontChangeDirection'])

            msg = directMessaging.get(
                messageType = DirectMessageType.activateSpeechBubble
            )  


    def moveRenderable(self, renderable, x :int =0, y :int =0, dontChangeDirection :bool =False):
        """Move this renderable in x/y direction, if allowed. Update direction too"""
        if x != 0 or y != 0:
            renderable.texture.advanceStep()

        if x > 0:
            if renderable.coordinates.x < Config.columns - renderable.texture.width - 1:
                renderable.coordinates.x += 1
                
                if not dontChangeDirection and renderable.direction is not Direction.right:
                    renderable.direction = Direction.right
                    renderable.texture.changeAnimation(
                        CharacterAnimationType.walking, renderable.direction)  

        elif x < 0:
            if renderable.coordinates.x > 1:
                renderable.coordinates.x -= 1
                if not dontChangeDirection and renderable.direction is not Direction.left:
                    renderable.direction = Direction.left
                    renderable.texture.changeAnimation(
                        CharacterAnimationType.walking, renderable.direction)    

        if y > 0:
            if renderable.coordinates.y < Config.rows - renderable.texture.height - 1:
                renderable.coordinates.y += 1
        
        elif y < 0:
            if renderable.coordinates.y >  Config.areaMoveable['miny'] - renderable.texture.height + 1:
                renderable.coordinates.y -= 1


    def speechBubbleActivator(self):
        msg = directMessaging.get(
            messageType = DirectMessageType.activateSpeechBubble
        )
        while msg is not None:
            for ent, (renderable, speechBubble, groupId) in self.world.get_components(
                system.renderable.Renderable, 
                system.graphics.speechbubble.SpeechBubble,
                system.groupid.GroupId
            ):
                if groupId.getId() == msg.groupId:
                    speechBubble.changeText(msg.data)

            msg = directMessaging.get(
                messageType = DirectMessageType.activateSpeechBubble
            )


    def advance(self, deltaTime):
        for ent, rend in self.world.get_component(system.renderable.Renderable):
            rend.advance(deltaTime)


    def collisionDetection(self): 
        for message in messaging.get():
            damageSum = 0

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

                # check if we should announce our awesomeness
                if damageSum > Config.announceDamage:
                    # find player
                    for ent, (groupId, player) in self.world.get_components(
                        system.groupid.GroupId, system.gamelogic.player.Player
                    ):
                        directMessaging.add(
                            groupId = groupId.getId(),
                            type = DirectMessageType.activateSpeechBubble,
                            data = 'Cowabunga!',
                        )

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