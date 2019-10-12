#!/usr/bin/env python

import unittest

from game.enemyloader import EnemyLoader
from game.enemytype import EnemyType
from texture.filetextureloader import fileTextureLoader
from texture.character.charactertexturetype import CharacterTextureType
from system.gamelogic.weapontype import WeaponType
import game.isunittest


class EnemyLoaderTest(unittest.TestCase):
    def test_loadEnemy(self):
        game.isunittest.setIsUnitTest()

        fileTextureLoader.loadFromFiles()
        enemyLoader = EnemyLoader()
        enemySeed = enemyLoader.getSeedForEnemy(EnemyType.unittest)

        self.assertTrue(enemySeed.characterTextureType
                        is CharacterTextureType.stickfigure)
        self.assertTrue(enemySeed.weaponType is WeaponType.hitSquare)
        self.assertTrue(enemySeed.health == 100)
        self.assertTrue(enemySeed.enemyInfo.attackWindupTime == 1.0)
        self.assertTrue(enemySeed.attackBaseLocation['x'] == -1)


if __name__ == '__main__':
    unittest.main()
