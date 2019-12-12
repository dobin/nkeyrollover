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
from texture.filetextureloader import fileTextureLoader
from utilities.entityfinder import EntityFinder
from tests.mockwin import MockWin
import game.isunittest
from system.gamelogic.movementprocessor import MovementProcessor
from system.io.inputprocessor import InputProcessor
from system.graphics.renderableminimalprocessor import RenderableMinimalProcessor
from system.graphics.renderableprocessor import RenderableProcessor
from utilities.entityfinder import EntityFinder
from system.graphics.physics import Physics
from system.singletons.particleemiter import ParticleEmiter

class RenderableTest(unittest.TestCase):
    def test_renderableBasic(self):
        game.isunittest.setIsUnitTest()
        fileTextureLoader.loadFromFiles()

        self.viewport = MockWin(20, 10)
        self.world = esper.World()
        self.textureEmiter = None
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

        p = Coordinates(9, 9)
        self.assertFalse(renderable.isHitBy([p]))
        p = Coordinates(13, 13)

        # in sprite, but dest is empty
        self.assertFalse(renderable.isHitBy([p]))
        p = Coordinates(10, 10)
        # in sprite, but on head (not empty)
        self.assertFalse(renderable.isHitBy([p]))
        p = Coordinates(11, 10)

        self.assertTrue(renderable.isHitBy([p]))
        p = Coordinates(12, 12)
        self.assertTrue(renderable.isHitBy([p]))

        renderable.setDirection(Direction.left)
        attackLocation = renderable.getAttackBaseLocation()
        self.assertTrue(attackLocation.x == 9)
        self.assertTrue(attackLocation.y == 11)

        attackLocation = renderable.getAttackBaseLocationInverted()
        self.assertTrue(attackLocation.x == 13)
        self.assertTrue(attackLocation.y == 11)


    def test_renderableDistanceToBorder(self):
        game.isunittest.setIsUnitTest()
        fileTextureLoader.loadFromFiles()

        self.viewport = MockWin(20, 10)
        self.world = esper.World()
        self.textureEmiter = None

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
        playerRenderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates,
            direction=Direction.right,
            name='Player')
        physics = Physics()

        self.world.add_component(playerEntity, playerRenderable)
        self.world.add_component(playerEntity, physics)
        # /Player

        # Enemy
        enemyEntity = self.world.create_entity()
        texture = CharacterTexture(
            characterTextureType=CharacterTextureType.player,
            characterAnimationType=CharacterAnimationType.standing,
            name='Enemy')

        coordinates = Coordinates(
            13,
            10
        )
        enemyRenderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates,
            direction=Direction.right,
            name='Enemy')
        physics = Physics()

        self.world.add_component(enemyEntity, enemyRenderable)
        self.world.add_component(playerEntity, physics)
        # /Enemy

        # process it
        targetFrameTime = 1.0 / Config.fps

        # x adjectant
        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertFalse(overlap)
        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertFalse(overlap)
        empty = EntityFinder.isDestinationEmpty(
            self.world, playerRenderable)
        self.assertTrue(empty)
        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == 0)
        self.assertTrue(distance['y'] == 0)
        ret = EntityFinder.isDestinationEmpty(
            self.world, enemyRenderable)
        self.assertTrue(ret)

        # x one space distance
        enemyRenderable.coordinates.x += 1
        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertFalse(overlap)
        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertFalse(overlap)
        empty = EntityFinder.isDestinationEmpty(
            self.world, playerRenderable)
        self.assertTrue(empty)
        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == 1)
        self.assertTrue(distance['y'] == 0)
        ret = EntityFinder.isDestinationEmpty(
            self.world, enemyRenderable)
        self.assertTrue(ret)

        # x inside 1
        #  o o      
        # /|/|\     
        # / / \ 
        enemyRenderable.coordinates.x -= 2
        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertTrue(overlap)
        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertTrue(overlap)
        empty = EntityFinder.isDestinationEmpty(
            self.world, enemyRenderable,)
        self.assertFalse(empty)
        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == -1)
        self.assertTrue(distance['y'] == 0)
        ret = EntityFinder.isDestinationEmpty(
            self.world, enemyRenderable)
        self.assertFalse(ret)

        # x inside 2
        enemyRenderable.coordinates.x -= 1
        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertTrue(overlap)
        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertTrue(overlap)
        empty = EntityFinder.isDestinationEmpty(
            self.world, enemyRenderable)
        self.assertFalse(empty)
        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == -2)
        self.assertTrue(distance['y'] == 0)
        ret = EntityFinder.isDestinationEmpty(
            self.world, enemyRenderable)
        self.assertFalse(ret)

        # y 2
        #      o
        #   o /|\
        #  /|\/ \
        #  / \
        enemyRenderable.coordinates.x += 2
        enemyRenderable.coordinates.y -= 1
        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertFalse(overlap)
        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertFalse(overlap)
        empty = EntityFinder.isDestinationEmpty(self.world, enemyRenderable)
        self.assertTrue(empty)
        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == 0)
        self.assertTrue(distance['y'] == -2)
        ret = EntityFinder.isDestinationEmpty(
            self.world, enemyRenderable)
        self.assertTrue(ret)

        # y 3
        enemyRenderable.coordinates.y -= 2
        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertFalse(overlap)
        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertFalse(overlap)
        empty = EntityFinder.isDestinationEmpty(self.world, enemyRenderable)
        self.assertTrue(empty)
        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == 0)
        self.assertTrue(distance['y'] == 0)

        # y above each other
        enemyRenderable.coordinates.x -= 3
        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertFalse(overlap)
        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertFalse(overlap)
        empty = EntityFinder.isDestinationEmpty(self.world, enemyRenderable)
        self.assertTrue(empty)
        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == 0)
        self.assertTrue(distance['y'] == 0)

        # directly on top of each other
        enemyRenderable.coordinates.y += 3
        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertTrue(overlap)
        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertTrue(overlap)
        empty = EntityFinder.isDestinationEmpty(self.world, enemyRenderable)
        self.assertFalse(empty)
        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == 0)
        self.assertTrue(distance['y'] == 0)

        # sprites overlap, but not with chars (foot is in shoulder)
        #               o
        #              /|\
        #             o/ \
        #            /|\
        #            / \
        enemyRenderable.coordinates.y -= 2
        enemyRenderable.coordinates.x += 2

        self.world.process(targetFrameTime)
        self.viewport.internalPrint()

        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertTrue(overlap)  # inprecise check, true

        #overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        overlap = playerRenderable.overlapsWithRenderablePixel(enemyRenderable)
        self.assertFalse(overlap)  # precise check, false

        # empty = EntityFinder.isDestinationEmpty(self.world, enemyRenderable, enemyRenderable.getLocationAndSize())
        empty = EntityFinder.isDestinationEmpty(self.world, playerRenderable)
        self.assertTrue(empty)

        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == -1)
        self.assertTrue(distance['y'] == -1)

        # self.world.process(targetFrameTime)
        # self.viewport.internalPrint()


    def test_renderableCollisionDetection(self):
        game.isunittest.setIsUnitTest()
        fileTextureLoader.loadFromFiles()

        self.viewport = MockWin(20, 10)
        self.world = esper.World()
        self.textureEmiter = None

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
        playerRenderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates,
            direction=Direction.right,
            name='Player')
        physics = Physics()

        self.world.add_component(playerEntity, playerRenderable)
        self.world.add_component(playerEntity, physics)
        # /Player

        # Enemy
        enemyEntity = self.world.create_entity()
        texture = CharacterTexture(
            characterTextureType=CharacterTextureType.player,
            characterAnimationType=CharacterAnimationType.standing,
            name='Enemy')

        coordinates = Coordinates(
            10,
            10
        )
        enemyRenderable = Renderable(
            texture=texture,
            viewport=self.viewport,
            parent=None,
            coordinates=coordinates,
            direction=Direction.right,
            name='Enemy')
        physics = Physics()

        self.world.add_component(enemyEntity, enemyRenderable)
        self.world.add_component(playerEntity, physics)
        # /Enemy

        # process it
        targetFrameTime = 1.0 / Config.fps

        # sprites overlap, but not with chars (foot is in shoulder)
        #               o
        #              /|\
        #             o/ \
        #            /|\
        #            / \
        enemyRenderable.coordinates.y -= 2
        enemyRenderable.coordinates.x += 2

        self.world.process(targetFrameTime)
        self.viewport.internalPrint()

        overlap = enemyRenderable.overlapsWith(playerRenderable)
        self.assertTrue(overlap)  # inprecise check, true

        overlap = playerRenderable.overlapsWithRenderablePixel(enemyRenderable)
        self.assertFalse(overlap)  # precise check, false

        overlap = enemyRenderable.overlapsWithRenderablePixel(playerRenderable)
        self.assertFalse(overlap)  # precise check, false

        empty = EntityFinder.isDestinationEmpty(
            self.world, enemyRenderable)
        self.assertTrue(empty)

        empty = EntityFinder.isDestinationEmpty(
            self.world, playerRenderable)
        self.assertTrue(empty)

        distance = enemyRenderable.distanceToBorder(playerRenderable)
        self.assertTrue(distance['x'] == -1)
        self.assertTrue(distance['y'] == -1)


if __name__ == '__main__':
    unittest.main()
