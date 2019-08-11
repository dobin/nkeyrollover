import unittest
import logging 

from tests.fakeworld import FakeWorld
import tests.mockcurses as curses
from entities.enemy.enemy import Enemy
from sprite.direction import Direction
from sprite.particle import Particle
from texture.phenomena.phenomenatexture import PhenomenaTexture
from texture.phenomena.phenomenatype import PhenomenaType
from config import Config
from sprite.coordinates import Coordinates
from sprite.sprite import Sprite


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

        p = Particle(viewport=world.viewport, x=basex, y=basey, life=30, 
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
        

    def test_texturecoordinates(self): 
        win = curses.newwin(Config.rows, Config.columns)
        world = FakeWorld(win)

        sprite = Sprite(viewport = world.viewport, parentSprite=None,
            coordinates=Coordinates(0,0), direction=Direction.left)


        texture :PhenomenaTexture = PhenomenaTexture(
            phenomenaType=PhenomenaType.hit, 
            parentSprite=sprite)
        texture.changeAnimation(PhenomenaType.hit, Direction.left)
        coords = texture.getTextureHitCoordinates()
        self.assertTrue(len(coords) == 1)
        self.assertTrue(coords[0].x == 0 and coords[0].y == 0)

        texture :PhenomenaTexture = PhenomenaTexture(
            phenomenaType=PhenomenaType.hitSquare,
            parentSprite=sprite)
        texture.changeAnimation(PhenomenaType.hitSquare, Direction.left)
        coords = texture.getTextureHitCoordinates()
        self.assertTrue(len(coords) == 4)
        self.assertTrue(coords[0].x == 0 and coords[0].y == 0)
        self.assertTrue(coords[1].x == 0 and coords[1].y == 1)
        self.assertTrue(coords[2].x == 1 and coords[2].y == 0)
        self.assertTrue(coords[3].x == 1 and coords[3].y == 1)
        




if __name__ == '__main__':
    unittest.main()