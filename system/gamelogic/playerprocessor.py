import esper
import curses
import logging
from enum import Enum

from ai.brain import Brain
from world.particleeffecttype import ParticleEffectType
from utilities.utilities import Utility
from config import Config
from entities.characterstatus import CharacterStatus
from sprite.direction import Direction
from entities.character import Character
from entities.entitytype import EntityType
from texture.character.charactertexture import CharacterTexture
from texture.character.characteranimationtype import CharacterAnimationType
from entities.weapontype import WeaponType
from sprite.coordinates import Coordinates, ExtCoordinates
from world.viewport import Viewport
#from world.world import World
#from entity.entity import Entity
from utilities.timer import Timer
from utilities.colorpalette import ColorPalette
from utilities.colortype import ColorType
from utilities.color import Color
from entities.player.state_attack import StateAttack
from entities.player.state_dying import StateDying
from entities.player.state_idle import StateIdle
from entities.player.state_spawn import StateSpawn
from entities.player.state_walking import StateWalking
from texture.character.charactertype import CharacterType
from messaging import messaging, Messaging, Message, MessageType

import system.advanceable 
import system.renderable
import system.gamelogic.player

from directmessaging import directMessaging, DirectMessage, DirectMessageType


class PlayerProcessor(esper.Processor):
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        self.advance(deltaTime)
        self.animationUpdateMove()
        self.animationUpdateAttack()


    def advance(self, deltaTime):
        for ent, player in self.world.get_component(
            system.gamelogic.player.Player
        ):
            player.advance(deltaTime)


    def animationUpdateMove(self):
        msg = directMessaging.get(
            messageType = DirectMessageType.entityMoved
        )
        while msg is not None:
            entity = Utility.findCharacterByGroupId(self.world, msg.groupId)
            playerRenderable = self.world.component_for_entity(
                entity, system.renderable.Renderable)

            if playerRenderable.texture.characterAnimationType is CharacterAnimationType.walking:
                if msg.data['didChangeDirection']:
                    playerRenderable.texture.changeAnimation(
                        CharacterAnimationType.walking,
                        playerRenderable.direction)
                else:
                    playerRenderable.texture.advanceStep()
            else:
                playerRenderable.texture.changeAnimation(
                    CharacterAnimationType.walking,
                    playerRenderable.direction)

            # Next message
            msg = directMessaging.get(
                messageType = DirectMessageType.entityMoved
            ) 


    def animationUpdateAttack(self):
        messages = messaging.get()
        for message in messages: 
            if message.type == MessageType.PlayerAttack:
                logging.info("AAAAAAA")
                playerEntity = Utility.findPlayer(self.world)
                playerRenderable = self.world.component_for_entity(
                    playerEntity, system.renderable.Renderable)

                playerRenderable.texture.changeAnimation(
                    CharacterAnimationType.hitting,
                    playerRenderable.direction)
