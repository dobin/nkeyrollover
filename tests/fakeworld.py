from entities.entity import Entity
from entities.player.player import Player
from world.director import Director
from entities.entitytype import EntityType
from world.particleemiter import ParticleEmiter
from sprite.sprite import Sprite
from world.viewport import Viewport


class FakeWorld(object): 
    def __init__(self, win): 
        self.win = win
        self.viewport = Viewport(win=win, world=self)
        self.worldSprite = Sprite(viewport=self.viewport, parentSprite=None)
        self.player = Player(win, self.worldSprite, None, self)
        self.director = Director(win, self) # real director
        self.particleEmiter = ParticleEmiter(self.win) # real particle emiter. for test_playerskill

    def getPlayer(self):
        return self.player

    def makeExplode(self, sprite, charDirection, data):
        pass