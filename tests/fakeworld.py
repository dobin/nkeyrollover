from entities.entity import Entity
from entities.player.player import Player
from world.director import Director
from entities.entitytype import EntityType
from world.particleemiter import ParticleEmiter
from sprite.sprite import Sprite

class FakeWorld(object): 
    def __init__(self, win): 
        self.win = win
        self.worldSprite = Sprite(win=win, parentSprite=None)
        self.player = Player(win, self.worldSprite, None, self)
        self.director = Director(win, self) # real director
        self.particleEmiter = ParticleEmiter(self.win) # real particle emiter. for test_playerskill

    def getPlayer(self):
        return self.player

    def makeExplode(self, sprite, charDirection, data):
        pass