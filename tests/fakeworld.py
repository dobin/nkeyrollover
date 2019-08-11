from entities.entity import Entity
from entities.player.player import Player
from world.director import Director
from entities.entitytype import EntityType
from world.particleemiter import ParticleEmiter
from sprite.sprite import Sprite
from world.viewport import Viewport

class FakeViewport(Viewport): 
    # used by hasttr() to check if unit test is being run
    def isUnitTest(self): 
        pass


class FakeWorld(object): 
    def __init__(self, win, fakeViewPort=True, withDirector=True): 
        self.win = win

        if fakeViewPort:
            self.viewport = FakeViewport(win=win, world=self)
        else: 
            self.viewport =  Viewport(win=win, world=self)

        self.worldSprite = Sprite(viewport=self.viewport, parentSprite=None)
        self.player = Player(win, self.worldSprite, None, self)

        if withDirector:
            self.director = Director(win, self) # real director
        else: 
            self.director = None
        self.particleEmiter = ParticleEmiter(self.win) # real particle emiter. for test_playerskill

    def getPlayer(self):
        return self.player

    def makeExplode(self, sprite, charDirection, data):
        pass