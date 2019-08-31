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
from system.advanceable import Advanceable
from system.renderable import Renderable
from texture.speechtexture import SpeechTexture

from messaging import messaging, Messaging, Message, MessageType


class tPlayer():
    def __init__(self, renderable):
        self.renderable = renderable

        # from character
        self.characterStatus = CharacterStatus()
        self.speechTexture = SpeechTexture(parentSprite=self, displayText='')
        self.speechTexture.setActive(False)

        # from player
        self.skills = PlayerSkills(player=self)
        self.initAi()
        self.name = 'Player'


    def initAi(self):
        self.brain = Brain(self.renderable)
        self.brain.register(StateIdle)
        self.brain.register(StateSpawn)
        self.brain.register(StateAttack)
        self.brain.register(StateWalking)
        self.brain.push("spawn")


    def announce(self, damage, particleEffectType): 
        text = ''
        if particleEffectType is ParticleEffectType.laser:
            text = 'Cowabunga!'

        if particleEffectType is ParticleEffectType.cleave:
            text = 'I\'ll be back!'

        if particleEffectType is ParticleEffectType.explosion:
            text = 'Boom baby!'

        if damage > Config.announceDamage: 
            self.speechTexture.changeAnimation(text)


    def advance(self, deltaTime):
        self.characterStatus.advance(deltaTime)
        self.speechTexture.advance(deltaTime)        
        self.brain.update(deltaTime)
        self.skills.advance(deltaTime)


    def __repr__(self): 
        return "Player"        


class tPlayerProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.movementTimer = Timer( 1.0 / Config.movementKeysPerSec, instant=True)


    def process(self, deltaTime):
        self.handleKeyboardInput()
        self.advance(deltaTime)


    def advance(self, deltaTime):
        self.movementTimer.advance(deltaTime)

        for ent, player in self.world.get_component(tPlayer):
            player.advance(deltaTime)


    def handleKeyboardInput(self):
        for ent, (renderable, player) in self.world.get_components(Renderable, tPlayer):
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

        if self.movementTimer.timeIsUp(): 
            if key == curses.KEY_LEFT:
                self.move(playerRenderable, player, x=-1, y=0)
                return True

            elif key == curses.KEY_RIGHT: 
                self.move(playerRenderable, player, x=1, y=0)
                return True

            elif key == curses.KEY_UP:
                self.move(playerRenderable, player, x=0, y=-1)
                return True

            elif key == curses.KEY_DOWN: 
                self.move(playerRenderable, player, x=0, y=1)
                return True

        return False


    def move(self, playerRenderable, player, x=0, y=0):
        currentDirection = playerRenderable.direction
        if x < 0:
            if Utility.isPointMovable(
                playerRenderable.coordinates.x - 1, 
                playerRenderable.coordinates.y, 
                playerRenderable.texture.width, 
                playerRenderable.texture.height
            ):
                playerRenderable.coordinates.x -= 1
                playerRenderable.direction = Direction.left
                self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )
        elif x > 0: 
            if Utility.isPointMovable(
                playerRenderable.coordinates.x + 1, 
                playerRenderable.coordinates.y, 
                playerRenderable.texture.width, 
                playerRenderable.texture.height
            ):
                playerRenderable.coordinates.x += 1
                playerRenderable.direction = Direction.right
                self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )

        if y < 0:
            if Config.moveDiagonal:
                if Utility.isPointMovable(
                    playerRenderable.coordinates.x + 1, 
                    playerRenderable.coordinates.y - 1, 
                    playerRenderable.texture.width, 
                    playerRenderable.texture.height
                ):
                    playerRenderable.coordinates.y -= 1
                    playerRenderable.coordinates.x += 1
                    self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )
            else: 
                if Utility.isPointMovable(
                    playerRenderable.coordinates.x, 
                    playerRenderable.coordinates.y - 1, 
                    playerRenderable.texture.width, 
                    playerRenderable.texture.height
                ):
                    playerRenderable.coordinates.y -= 1
                    self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )
        if y > 0: 
            if Config.moveDiagonal:
                if Utility.isPointMovable(
                    playerRenderable.coordinates.x - 1, 
                    playerRenderable.coordinates.y + 1, 
                    playerRenderable.texture.width, 
                    playerRenderable.texture.height
                ):
                    playerRenderable.coordinates.y += 1
                    playerRenderable.coordinates.x -= 1
                    self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )
            else:
                if Utility.isPointMovable(
                    playerRenderable.coordinates.x, 
                    playerRenderable.coordinates.y + 1, 
                    playerRenderable.texture.width, 
                    playerRenderable.texture.height
                ):
                    playerRenderable.coordinates.y += 1
                    self.movePlayer(playerRenderable, player, currentDirection == playerRenderable.direction )

        extcords = ExtCoordinates(
            playerRenderable.coordinates.x,
            playerRenderable.coordinates.y,
            playerRenderable.texture.width,
            playerRenderable.texture.height)
        messaging.add(
            type=MessageType.PlayerLocation, 
            data=extcords)


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