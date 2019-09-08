#!/usr/bin/env python

import unittest
import esper

import system.gamelogic.player
from messaging import messaging, MessageType
from common.coordinates import Coordinates
from config import Config
from texture.character.charactertype import CharacterType
from texture.character.charactertexture import CharacterTexture
from entities.esperdata import EsperData
from texture.character.characteranimationtype import CharacterAnimationType
from system.graphics.renderable import Renderable
from system.gamelogic.offensiveskill import OffensiveSkill
from system.groupid import GroupId
from system.gamelogic.attackable import Attackable
from system.gamelogic.offensiveattack import OffensiveAttack
from utilities.entityfinder import EntityFinder
from system.gamelogic.player import Player

from tests.mockwin import MockWin
import world.isunittest
from system.gamelogic.movementprocessor import MovementProcessor
from system.io.inputprocessor import InputProcessor
from system.graphics.renderableminimalprocessor import RenderableMinimalProcessor
from system.graphics.renderableprocessor import RenderableProcessor



class RenderableTest(unittest.TestCase):
    def test_renderable(self):
        world.isunittest.setIsUnitTest()

        self.viewport = MockWin(20, 10)
        self.particleEmiter = None
        self.world = esper.World()
        self.textureEmiter = None

        renderableProcessor = RenderableProcessor()
        movementProcessor = MovementProcessor()
        inputProcessor = InputProcessor()
        renderableMinimalProcessor = RenderableMinimalProcessor(
            viewport=self.viewport,
            textureEmiter=self.textureEmiter)
        self.world.add_processor(inputProcessor)
        self.world.add_processor(movementProcessor)
        self.world.add_processor(renderableMinimalProcessor)
        self.world.add_processor(renderableProcessor)


        # Player


        # process it
        targetFrameTime = 1.0 / Config.fps
        self.world.process(targetFrameTime)
        self.viewport.internalPrint()
        #self.world.process(targetFrameTime)
        #self.viewport.internalPrint()


if __name__ == '__main__':
    unittest.main()