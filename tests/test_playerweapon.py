#!/usr/bin/env python

import unittest
import time
import logging
import curses

from entities.characterattack import CharacterAttack
from entities.entity import Entity
from entities.entitytype import EntityType
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from config import Config
from world.director import Director
from sprite.direction import Direction
from tests.fakeworld import FakeWorld
from sprite.coordinates import Coordinates
from utilities.utilities import Utility


class PlayerWeaponTest(unittest.TestCase):

    def test_weaponHit(self):
        """Simple hitting an enemy right of the player with standard weapon"""
        Utility.setupLogger()
        
        win = None
        world = FakeWorld(win, fakeViewPort=True)

        # set player
        world.getPlayer().setLocation( Coordinates(10, 10))
        world.getPlayer().direction = Direction.right

        # set enemies
        enemy = Enemy(viewport=world.viewport, parent=world.worldSprite, 
            spawnBoundaries=None, world=world, name='bot')
        enemy.setLocation(Coordinates(13, 10))
        world.director.enemiesAlive.append(enemy)

        # action!
        life1 = enemy.characterStatus.health
        world.getPlayer().handleInput(ord('1')) # select first weapon
        world.getPlayer().advance(0.1)
        enemy.advance(0.1)
        world.getPlayer().handleInput(ord(' ')) # fire
        life2 = enemy.characterStatus.health
        self.assertLess(life2, life1)


    def test_weaponHitLine(self):
        """hitting an enemy left of the player with the line gun"""
        Utility.setupLogger()
        
        win = None
        world = FakeWorld(win)

        # player
        world.getPlayer().setLocation(Coordinates(10, 10))
        world.getPlayer().direction = Direction.left

        # enemy
        enemy = Enemy(viewport=world.viewport, parent=world.worldSprite, 
            spawnBoundaries=None, world=world, name='bot')
        enemy.setLocation(Coordinates(4, 10))
        world.director.enemiesAlive.append(enemy)

        # action!
        life1 = enemy.characterStatus.health
        world.getPlayer().handleInput(ord('3')) # select third weapon
        world.getPlayer().advance(0.1)
        enemy.advance(0.1)
        world.getPlayer().handleInput(ord(' ')) # fire
        life2 = enemy.characterStatus.health
        self.assertLess(life2, life1)


if __name__ == '__main__':
    unittest.main()