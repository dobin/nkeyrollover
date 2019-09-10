#!/usr/bin/env python

import unittest

from texture.filetextureloader import FileTextureLoader
from texture.phenomena.phenomenatype import PhenomenaType
import game.isunittest


class FileTextureLoaderTest(unittest.TestCase):
    def test_loadTexture(self):
        game.isunittest.setIsUnitTest()

        fileTextureLoader = FileTextureLoader()
        animation = fileTextureLoader.readPhenomena(PhenomenaType.unittest)

        self.assertTrue(animation.height == 2)
        self.assertTrue(animation.width == 2)
        self.assertTrue(animation.frameCount == 2)

        self.assertTrue(animation.endless is True)
        self.assertTrue(animation.advanceByStep is False)
        self.assertTrue(animation.frameTime[0] == 0.1)
        self.assertTrue(animation.frameTime[1] == 0.2)
        self.assertTrue(animation.frameColors[0] == 'white')
        self.assertTrue(animation.frameColors[1] == 'green')

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


if __name__ == '__main__':
    unittest.main()