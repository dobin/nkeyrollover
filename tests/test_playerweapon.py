#!/usr/bin/env python

import unittest
import time

from entities.player.playerweapon import PlayerWeapon
from entities.entity import Entity
from entities.entitytype import EntityType


class PlayerWeaponTest(unittest.TestCase):
    def test_weaponAnimation(self):
        entity = Entity(win=None, parentEntity=None, entityType=EntityType.player)
        playerWeapon = PlayerWeapon(win=None, parentCharacter=entity)

    def test_weaponHit(self):
        pass


if __name__ == '__main__':
    unittest.main()