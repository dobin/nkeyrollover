from entities.entity import Entity
from entities.player.player import Player
from world.director import Director
from entities.entitytype import EntityType
from world.particleemiter import ParticleEmiter

class FakeWorld(object): 
    def __init__(self, win): 
        self.win = win
        self.worldEntity = Entity(win=win, parentEntity=None, entityType=EntityType.world)
        self.player = Player(win, self.worldEntity, None, self)
        self.director = Director(win, self) # real director
        self.particleEmiter = ParticleEmiter(self.win) # real particle emiter. for test_playerskill

    def getPlayer(self):
        return self.player

    def makeExplode(self, sprite, charDirection, data):
        pass