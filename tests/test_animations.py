import unittest
import logging 

from tests.fakeworld import FakeWorld
from entities.direction import Direction
from entities.enemy.enemy import Enemy
from sprite.particle import Particle
import tests.mockcurses as curses
from config import Config


class AnimationTest(unittest.TestCase):
    def test_animationParticle(self): 
        # check if area skill hits enemy 
        win = curses.newwin(Config.rows, Config.columns)
        world = FakeWorld(win)

        logging.basicConfig(
            filename='app.log', 
            filemode='a', 
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)07s %(name)32s: %(message)s')

        basex = 20
        basey = 20

        p = Particle(win=win, x=basex, y=basey, life=30, 
            angle=180, speed=0.2, active=True)
        win.border()

        p.advance(0.02)
        win.clear()
        p.draw()
        # win.draw()

        self.assertFalse( win.peek(basex, basey) == '' )
        self.assertTrue( win.peek(basex-1, basey) == '' )
        self.assertTrue( win.peek(basex-2, basey) == '' )

        p.advance(0.01)
        win.clear()
        p.draw()
        # win.draw()

        self.assertTrue( win.peek(basex, basey) == '' )
        self.assertFalse( win.peek(basex-1, basey) == '' )
        self.assertTrue( win.peek(basex-2, basey) == '' )

        p.advance(0.06)
        win.clear()
        p.draw()
        # win.draw()

        self.assertTrue( win.peek(basex, basey) == '' )
        self.assertTrue( win.peek(basex-1, basey) == '' )
        self.assertFalse( win.peek(basex-2, basey) == '' )
        


if __name__ == '__main__':
    unittest.main()