#!/usr/bin/env python

import unittest
import time

from entities.characterattack import CharacterAttack
from entities.entity import Entity
from entities.entitytype import EntityType
from entities.player.player import Player
from entities.enemy.enemy import Enemy
from config import Config
from director import Director
from entities.direction import Direction

import logging
import curses

class FakeWorld(object): 
    def __init__(self, win): 
        self.win = win
        self.worldEntity = Entity(win=win, parentEntity=None, entityType=EntityType.world)
        self.player = Player(win, self.worldEntity, None, self)
        self.director = Director(win, self) # real director

    def getPlayer(self):
        return self.player




class PlayerWeaponTest(unittest.TestCase):
    def test_weaponAnimation(self):
        pass

    def test_weaponHit(self):
        # Simple hitting an enemy right of the player with
        # standard weapon
        win = None
        world = FakeWorld(win)
        world.player.setLocation(10, 10)

        enemy = Enemy(win, world.worldEntity, None, world, 'bot')
        enemy.setLocation(13, 10)
        world.director.enemiesAlive.append(enemy)

        life1 = enemy.characterStatus.health

        world.player.handleInput(ord('1')) # select first weapon
        world.player.advance(0.1)
        enemy.advance(0.1)
        world.player.handleInput(ord(' ')) # fire
        
        life2 = enemy.characterStatus.health
        
        self.assertLess(life2, life1)


    def test_weaponHitLine(self):
        # hitting an enemy left of the player with the line gun
        win = None
        world = FakeWorld(win)
        world.player.setLocation(10, 10)
        world.player.direction = Direction.left

        enemy = Enemy(win, world.worldEntity, None, world, 'bot')
        enemy.setLocation(4, 10)
        world.director.enemiesAlive.append(enemy)

        life1 = enemy.characterStatus.health

        world.player.handleInput(ord('3')) # select third weapon
        world.player.advance(0.1)
        enemy.advance(0.1)
        world.player.handleInput(ord(' ')) # fire
        
        life2 = enemy.characterStatus.health
        
        self.assertLess(life2, life1)




if __name__ == '__main__':
    unittest.main()