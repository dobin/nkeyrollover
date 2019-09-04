#!/usr/bin/env python

import unittest
import time
import logging
import curses

from texture.filetextureloader import FileTextureLoader


class FileTextureLoaderTest(unittest.TestCase):
    def test_loadTexture(self): 
        fileTextureLoader = FileTextureLoader()

        animation = fileTextureLoader.readPhenomena('unittest')

        self.assertTrue(animation.height == 2)
        self.assertTrue(animation.width == 2)
        self.assertTrue(animation.frameCount == 2)

        self.assertTrue(animation.endless == True)
        self.assertTrue(animation.advanceByStep == True)
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