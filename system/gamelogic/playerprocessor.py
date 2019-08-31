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
from entities.player.playerskills import PlayerSkills
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
from texture.speechtexture import SpeechTexture
from messaging import messaging, Messaging, Message, MessageType

import system.advanceable 
import system.renderable
import system.gamelogic.player


class PlayerProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.movementTimer = Timer( 1.0 / Config.movementKeysPerSec, instant=True)


    def process(self, deltaTime):
        self.handleKeyboardInput()
        self.advance(deltaTime)


    def advance(self, deltaTime):
        self.movementTimer.advance(deltaTime)

        for ent, player in self.world.get_component(
            system.gamelogic.player.Player
        ):
            player.advance(deltaTime)


    def handleKeyboardInput(self):
        for ent, (renderable, player) in self.world.get_components(
            system.renderable.Renderable, system.gamelogic.player.Player
        ):
            didMove = False
            
            for message in messaging.get():
                if message.type is MessageType.PlayerKeypress:
                    didMoveTmp = self.handleKeyPress(message.data, player, renderable)
                    if didMoveTmp: 
                        didMove = True

            # to allow diagonal movement, we allow multiple movement keys per input
            # cycle, without resetting the timer.
            if didMove: 
                self.movementTimer.reset()


    def handleKeyPress(self, key, player, playerRenderable):
        # move to attack animation state
        if key == ord(' '):
            player.brain.pop()
            player.brain.push('attack')

        didMove = False
        if self.movementTimer.timeIsUp(): 
            if key == curses.KEY_LEFT:
                playerRenderable.move(x=-1, y=0)
                didMove = True

            elif key == curses.KEY_RIGHT: 
                playerRenderable.move(x=1, y=0)
                didMove = True

            elif key == curses.KEY_UP:
                playerRenderable.move(x=0, y=-1)
                didMove = True

            elif key == curses.KEY_DOWN: 
                playerRenderable.move(x=0, y=1)
                didMove = True

        if didMove:
            extcords = ExtCoordinates(
                playerRenderable.coordinates.x,
                playerRenderable.coordinates.y,
                playerRenderable.texture.width,
                playerRenderable.texture.height)
            messaging.add(
                type=MessageType.PlayerLocation, 
                data=extcords)
        
        return didMove


    def movePlayer(self, playerRenderable, player, sameDirection):
        if not sameDirection:
            playerRenderable.texture.changeAnimation(
                CharacterAnimationType.walking, playerRenderable.direction)

        # walking animation
        playerRenderable.advanceStep()

        currentState = player.brain.state
        if currentState.name == 'walking': 
            # keep him walking a bit more
            currentState.setTimer(1.0)
        else: 
            player.brain.pop()
            player.brain.push('walking')
