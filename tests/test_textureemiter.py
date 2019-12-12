#!/usr/bin/env python

import unittest
import esper

from messaging import messaging, MessageType
from common.coordinates import Coordinates
from config import Config

from tests.mockwin import MockWin
import game.isunittest
from system.gamelogic.movementprocessor import MovementProcessor
from system.io.inputprocessor import InputProcessor
from system.graphics.renderableminimalprocessor import RenderableMinimalProcessor
from system.graphics.renderableprocessor import RenderableProcessor
from game.textureemiter import TextureEmiter
from texture.action.actiontype import ActionType
from common.direction import Direction
from system.singletons.renderablecache import renderableCache
from texture.filetextureloader import fileTextureLoader
from system.singletons.particleemiter import ParticleEmiter

class TextureEmiterTest(unittest.TestCase):
    def test_actionemiter(self):
        game.isunittest.setIsUnitTest()

        fileTextureLoader.loadFromFiles()
        self.viewport = MockWin(20, 10)
        self.world = esper.World()
        self.textureEmiter = TextureEmiter(viewport=self.viewport, world=self.world)
        renderableCache.init(viewport=self.viewport)
        particleEmiter = ParticleEmiter(viewport=self.viewport)

        renderableProcessor = RenderableProcessor(
            textureEmiter=self.textureEmiter,
            particleEmiter=particleEmiter)
        movementProcessor = MovementProcessor(mapManager=None)
        inputProcessor = InputProcessor()
        renderableMinimalProcessor = RenderableMinimalProcessor(
            viewport=self.viewport,
            textureEmiter=self.textureEmiter)
        self.world.add_processor(inputProcessor)
        self.world.add_processor(movementProcessor)
        self.world.add_processor(renderableMinimalProcessor)
        self.world.add_processor(renderableProcessor)

        location = Coordinates(10, 10)
        self.textureEmiter.makeActionTexture(
            actionTextureType = ActionType.unittest,
            location=location,
            fromPlayer=True,
            direction=Direction.right,
            physics=None
        )

        messages = messaging.getByType(MessageType.PlayerAttack)
        for message in messages:
            print(message.data['hitLocations'])
            hl = message.data['hitLocations']

            self.assertTrue(hl[0].x == 12)
            self.assertTrue(hl[0].y == 11)

            self.assertTrue(hl[1].x == 12)
            self.assertTrue(hl[1].y == 12)

            self.assertTrue(hl[2].x == 13)
            self.assertTrue(hl[2].y == 11)

            self.assertTrue(hl[3].x == 13)
            self.assertTrue(hl[3].y == 12)


        # process it
        targetFrameTime = 1.0 / Config.fps
        self.world.process(targetFrameTime)

        self.assertTrue(self.viewport.peek(12, 11) == '>')
        self.assertTrue(self.viewport.peek(12, 12) == '>')
        self.assertTrue(self.viewport.peek(13, 11) == '>')
        self.assertTrue(self.viewport.peek(13, 12) == '>')

        self.world.process(0.1)  # animation len

        self.assertTrue(self.viewport.peek(12, 11) == '-')
        self.assertTrue(self.viewport.peek(12, 12) == '-')
        self.assertTrue(self.viewport.peek(13, 11) == '-')
        self.assertTrue(self.viewport.peek(13, 12) == '-')


if __name__ == '__main__':
    unittest.main()
