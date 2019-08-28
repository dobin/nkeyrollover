import unittest

from tests.fakeworld import FakeWorld
from sprite.direction import Direction
from entities.enemy.enemy import Enemy
from sprite.coordinates import Coordinates
from utilities.utilities import Utility

class PlayerSkillTest(unittest.TestCase):
    """check if area skill hits enemy"""
    def test_playerskill(self): 
        Utility.setupLogger()
        
        win = None
        world = FakeWorld(win, fakeViewPort=True)

        # player
        world.getPlayer().setLocation(Coordinates(10, 10))
        world.getPlayer().direction = Direction.left

        # enemy
        enemy = Enemy(viewport=world.viewport, parent=world.worldSprite, 
            spawnBoundaries=None, world=world, name='bot')
        enemy.setLocation(Coordinates(10-2, 10))
        world.director.enemiesAlive.append(enemy)

        # lets attack
        life1 = enemy.characterStatus.health
        world.getPlayer().handleInput(ord('r')) # fire explosion
        world.getPlayer().advance(0.1)
        enemy.advance(0.1)
        life2 = enemy.characterStatus.health
        self.assertLess(life2, life1)


if __name__ == '__main__':
    unittest.main()