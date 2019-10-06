#!/usr/bin/env python

import unittest

from common.direction import Direction
from game.offenseloader.fileoffenseloader import fileOffenseLoader
from texture.filetextureloader import fileTextureLoader

from texture.action.actiontype import ActionType
from system.gamelogic.weapontype import WeaponType
import game.isunittest
from system.singletons.renderablecache import renderableCache


class FileOffenseLoaderTest(unittest.TestCase):
    def test_loadWeapon(self):
        game.isunittest.setIsUnitTest()

        fileTextureLoader.loadFromFiles()
        fileOffenseLoader.loadFromFiles()
        renderableCache.init(viewport=None)
        weaponData = fileOffenseLoader.weaponManager.getWeaponData(
            WeaponType.unittest)

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
