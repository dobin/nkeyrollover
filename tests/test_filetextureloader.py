#!/usr/bin/env python

import unittest

from common.direction import Direction
from texture.filetextureloader import FileTextureLoader
from texture.phenomena.phenomenatype import PhenomenaType
from texture.action.actiontype import ActionType
from system.gamelogic.weapontype import WeaponType
import game.isunittest
from system.singletons.renderablecache import renderableCache


class FileTextureLoaderTest(unittest.TestCase):
    def test_loadTexturePhenomena(self):
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


    def test_loadTextureAction(self):
        game.isunittest.setIsUnitTest()

        fileTextureLoader = FileTextureLoader()
        animation = fileTextureLoader.readAction(ActionType.unittest)

        self.assertTrue(animation.height == 3)
        self.assertTrue(animation.width == 4)
        self.assertTrue(animation.frameCount == 3)

        self.assertTrue(animation.endless is False)
        self.assertTrue(animation.advanceByStep is False)
        self.assertTrue(animation.frameTime[0] == 0.1)
        self.assertTrue(animation.frameTime[1] == 0.1)
        self.assertTrue(animation.frameTime[2] == 0.1)
        self.assertTrue(animation.frameColors[0] == 'brightyellow')
        self.assertTrue(animation.frameColors[1] == 'brightyellow')
        self.assertTrue(animation.frameColors[2] == 'brightyellow')

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


    def test_loadWeapon(self):
        game.isunittest.setIsUnitTest()

        fileTextureLoader = FileTextureLoader()
        renderableCache.init(viewport=None)
        weaponData = fileTextureLoader.readWeapon(WeaponType.unittest)

        self.assertTrue(weaponData.actionTextureType is ActionType.unittest)
        self.assertTrue(weaponData.hitDetectionDirection == Direction.left)
        self.assertTrue(weaponData.damage == 10)

        self.assertTrue(weaponData.weaponHitArea[Direction.left].width == 5)
        self.assertTrue(weaponData.weaponHitArea[Direction.left].height == 3)

        self.assertTrue(weaponData.weaponHitArea[Direction.left].hitCd[0].x == 1)
        self.assertTrue(weaponData.weaponHitArea[Direction.left].hitCd[0].y == 0)

        self.assertTrue(weaponData.weaponHitArea[Direction.left].hitCd[1].x == 3)
        self.assertTrue(weaponData.weaponHitArea[Direction.left].hitCd[1].y == 0)

        self.assertTrue(weaponData.weaponHitArea[Direction.left].hitCd[2].x == 0)
        self.assertTrue(weaponData.weaponHitArea[Direction.left].hitCd[2].y == 1)

        self.assertTrue(weaponData.weaponHitArea[Direction.left].hitCd[5].x == 3)
        self.assertTrue(weaponData.weaponHitArea[Direction.left].hitCd[5].y == 2)


if __name__ == '__main__':
    unittest.main()
