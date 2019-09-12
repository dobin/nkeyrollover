#!/usr/bin/env python

import unittest
import esper

from common.coordinates import Coordinates
from config import Config
from texture.character.charactertexturetype import CharacterTextureType
from texture.character.charactertexture import CharacterTexture
from texture.character.characteranimationtype import CharacterAnimationType
from system.graphics.renderable import Renderable
from common.direction import Direction

from tests.mockwin import MockWin
import game.isunittest
from system.gamelogic.movementprocessor import MovementProcessor
from system.io.inputprocessor import InputProcessor
from system.graphics.renderableminimalprocessor import RenderableMinimalProcessor
from system.graphics.renderableprocessor import RenderableProcessor


class RenderableTest(unittest.TestCase):
    def test_renderable(self):
        game.isunittest.setIsUnitTest()

        self.viewport = MockWin(20, 10)
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
        playerEntity = self.world.create_entity()

        texture = CharacterTexture(
            characterTextureType=CharacterTextureType.player,
            characterAnimationType=CharacterAnimationType.standing,
            name='Player')

        coordinates = Coordinates(
            10,
            10
        )
        renderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates,
            direction=Direction.right,
            name='Player')

        self.world.add_component(playerEntity, renderable)
        # /Player

        # process it
        targetFrameTime = 1.0 / Config.fps
        self.world.process(targetFrameTime)
        self.viewport.internalPrint()

        # check if head is at correct position
        self.assertTrue(self.viewport.peek(11, 10) == 'o')

        extCoords = renderable.getLocationAndSize()
        self.assertTrue(extCoords.x == 10)
        self.assertTrue(extCoords.y == 10)
        self.assertTrue(extCoords.width == 3)
        self.assertTrue(extCoords.height == 3)

        locCenter = renderable.getLocationCenter()
        self.assertTrue(locCenter.x == 11)
        self.assertTrue(locCenter.y == 11)
        self.assertTrue(self.viewport.peek(11, 11) == '|')  # body

        attackLocation = renderable.getAttackBaseLocation()
        self.assertTrue(attackLocation.x == 13)
        self.assertTrue(attackLocation.y == 11)

        attackLocation = renderable.getAttackBaseLocationInverted()
        self.assertTrue(attackLocation.x == 9)
        self.assertTrue(attackLocation.y == 11)

        weaponBaseLoc = renderable.getWeaponBaseLocation()
        self.assertTrue(weaponBaseLoc.x == 12)
        self.assertTrue(weaponBaseLoc.y == 9)

        p = Coordinates(9, 9)
        self.assertFalse(renderable.isHitBy([p]))
        p = Coordinates(13, 13)
        self.assertFalse(renderable.isHitBy([p]))
        p = Coordinates(10, 10)
        self.assertTrue(renderable.isHitBy([p]))
        p = Coordinates(12, 12)
        self.assertTrue(renderable.isHitBy([p]))

        renderable.setDirection(Direction.left)
        attackLocation = renderable.getAttackBaseLocation()
        self.assertTrue(attackLocation.x == 9)
        self.assertTrue(attackLocation.y == 11)


if __name__ == '__main__':
    unittest.main()
