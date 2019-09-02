import esper
import copy
import logging
from typing import List

from sprite.coordinates import Coordinates, ExtCoordinates
from entities.character import Character
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.timer import Timer
from utilities.color import Color
from sprite.direction import Direction
from texture.character.characteranimationtype import CharacterAnimationType
from messaging import messaging, Messaging, Message, MessageType
from config import Config
from utilities.utilities import Utility

import system.gamelogic.attackable
import system.gamelogic.enemy
import system.gamelogic.player
import system.renderable
import system.groupid

from directmessaging import directMessaging, DirectMessage, DirectMessageType


logger = logging.getLogger(__name__)


class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, dt):
        self.move()


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
                didMove = self.moveRenderable(renderable, msg.data['x'], msg.data['y'])

                if didMove:
                    extcords = ExtCoordinates(
                        renderable.coordinates.x,
                        renderable.coordinates.y,
                        renderable.texture.width,
                        renderable.texture.height)
                    messaging.add(
                        type=MessageType.PlayerLocation, 
                        data=extcords)

                msg = directMessaging.get(
                    messageType = DirectMessageType.movePlayer
                )  

        # enemies
        msg = directMessaging.get(
            messageType = DirectMessageType.moveEnemy
        )
        while msg is not None:
            entity = Utility.findByGroupId(self.world, msg.groupId)
            meRenderable = self.world.component_for_entity(
                entity, system.renderable.Renderable)            
            self.moveRenderable(
                meRenderable, 
                msg.data['x'], 
                msg.data['y'], 
                msg.data['dontChangeDirection'])

            msg = directMessaging.get(
                messageType = DirectMessageType.moveEnemy
            )  


    def moveRenderable(self, renderable, x :int =0, y :int =0, dontChangeDirection :bool =False):
        """Move this renderable in x/y direction, if allowed. Update direction too"""
        didMove = False
        if x != 0 or y != 0:
            renderable.texture.advanceStep()

        if x > 0:
            if renderable.coordinates.x < Config.columns - renderable.texture.width - 1:
                renderable.coordinates.x += 1
                didMove = True
                
                if not dontChangeDirection and renderable.direction is not Direction.right:
                    renderable.direction = Direction.right
                    renderable.texture.changeAnimation(
                        CharacterAnimationType.walking, renderable.direction)  

        elif x < 0:
            if renderable.coordinates.x > 1:
                renderable.coordinates.x -= 1
                didMove = True
                if not dontChangeDirection and renderable.direction is not Direction.left:
                    renderable.direction = Direction.left
                    renderable.texture.changeAnimation(
                        CharacterAnimationType.walking, renderable.direction)    

        if y > 0:
            if renderable.coordinates.y < Config.rows - renderable.texture.height - 1:
                renderable.coordinates.y += 1
                didMove = True
        
        elif y < 0:
            if renderable.coordinates.y >  Config.areaMoveable['miny'] - renderable.texture.height + 1:
                renderable.coordinates.y -= 1
                didMove = True

        return didMove