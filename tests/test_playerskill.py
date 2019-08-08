import unittest

from tests.fakeworld import FakeWorld
from entities.direction import Direction
from entities.enemy.enemy import Enemy


class PlayerSkillTest(unittest.TestCase):
    def test_playerskill(self): 
        # check if area skill hits enemy 
        win = None
        world = FakeWorld(win)
        world.player.setLocation(10, 10)
        world.player.direction = Direction.left

        enemy = Enemy(win, world.worldEntity, None, world, 'bot')
        enemy.setLocation(10-2, 10)
        world.director.enemiesAlive.append(enemy)

        life1 = enemy.characterStatus.health

        world.player.handleInput(ord('r')) # fire explosion
        world.player.advance(0.1)
        enemy.advance(0.1)
        
        life2 = enemy.characterStatus.health
        
        self.assertLess(life2, life1)


if __name__ == '__main__':
    unittest.main()