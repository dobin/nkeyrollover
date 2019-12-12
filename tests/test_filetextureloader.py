#!/usr/bin/env python

import unittest

from common.direction import Direction
from texture.filetextureloader import fileTextureLoader
from texture.phenomena.phenomenatype import PhenomenaType
from texture.action.actiontype import ActionType
import game.isunittest


class FileTextureLoaderTest(unittest.TestCase):
    def test_loadTexturePhenomena(self):
        game.isunittest.setIsUnitTest()
        fileTextureLoader.loadFromFiles()
        animation = fileTextureLoader.phenomenaAnimationManager.readPhenomena(
            PhenomenaType.unittest)

        self.assertTrue(animation.height == 2)
        self.assertTrue(animation.width == 2)
        self.assertTrue(animation.frameCount == 2)

        self.assertTrue(animation.endless is True)
        self.assertTrue(animation.advanceByStep is False)
        self.assertTrue(animation.frameTime[0] == 0.1)
        self.assertTrue(animation.frameTime[1] == 0.2)
        self.assertTrue(animation.frameColors[0][0] == 'white')
        self.assertTrue(animation.frameColors[1][0] == 'green')

        x = 0
        y = 0
        frameIndex = 0
        self.assertTrue(animation.arr[frameIndex][y][x] == 'A')

        x = 1
        y = 0
        self.assertTrue(animation.arr[frameIndex][y][x] == 'B')

        x = 0
        y = 1
        self.assertTrue(animation.arr[frameIndex][y][x] == 'C')

        x = 1
        y = 1
        self.assertTrue(animation.arr[frameIndex][y][x] == 'D')

        x = 0
        y = 1
        frameIndex = 1
        self.assertTrue(animation.arr[frameIndex][y][x] == 'X')


    def test_loadTextureAction(self):
        game.isunittest.setIsUnitTest()

        fileTextureLoader.loadFromFiles()
        animation = fileTextureLoader.actionAnimationManager.getAnimation(
            ActionType.unittest, Direction.left)

        self.assertTrue(animation.height == 3)
        self.assertTrue(animation.width == 4)
        self.assertTrue(animation.frameCount == 3)

        self.assertTrue(animation.endless is False)
        self.assertTrue(animation.advanceByStep is False)
        self.assertTrue(animation.frameTime[0] == 0.1)
        self.assertTrue(animation.frameTime[1] == 0.1)
        self.assertTrue(animation.frameTime[2] == 0.1)
        self.assertTrue(animation.frameColors[0][0] == 'brightyellow')
        self.assertTrue(animation.frameColors[1][0] == 'brightyellow')
        self.assertTrue(animation.frameColors[2][0] == 'brightyellow')

        x = 0
        y = 1
        frameIndex = 0
        self.assertTrue(animation.arr[frameIndex][y][x] == '<')

        x = 1
        y = 1
        self.assertTrue(animation.arr[frameIndex][y][x] == '<')

        x = 0
        y = 2
        self.assertTrue(animation.arr[frameIndex][y][x] == '<')

        x = 1
        y = 2
        self.assertTrue(animation.arr[frameIndex][y][x] == '<')

        frameIndex = 1
        self.assertTrue(animation.arr[frameIndex][1][0] == '-')
        self.assertTrue(animation.arr[frameIndex][1][1] == '-')
        self.assertTrue(animation.arr[frameIndex][2][0] == '-')
        self.assertTrue(animation.arr[frameIndex][2][1] == '-')

        frameIndex = 2
        self.assertTrue(animation.arr[frameIndex][1][0] == '<')
        self.assertTrue(animation.arr[frameIndex][1][1] == '')
        self.assertTrue(animation.arr[frameIndex][2][0] == '<')
        self.assertTrue(animation.arr[frameIndex][2][1] == '')


if __name__ == '__main__':
    unittest.main()
