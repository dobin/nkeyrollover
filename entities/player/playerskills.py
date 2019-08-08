from config import Config
from world.particleeffecttype import ParticleEffectType
from texture.characteranimationtype import CharacterAnimationType
from utilities.timer import Timer

class PlayerSkills(object): 
    def __init__(self, player): 
        self.player = player
        self.skillStatus = [
            'q', 'w', 'e', 'r'
        ]
        self.cooldownTimers = {
            'q': Timer(1.0, instant=True),
            'w': Timer(1.0, instant=True),
            'e': Timer(1.0, instant=True),
            'r': Timer(1.0, instant=True),
        }


    def doSkill(self, key): 
        if key == 'q': 
            self.player.actionCtrl.changeTo(
                CharacterAnimationType.shrugging, 
                self.player.direction)
        
        if key == 'w':
            self.player.speechSprite.changeTexture('hoi')

        if key == 'e':
            self.skillSwitchSide()

        if key == 'r':
            if self.isRdy(key): 
                self.skillExplosion()
                self.cooldownTimers[key].reset()


    def isRdy(self, skill):
        return self.cooldownTimers[skill].timeIsUp()


    def skillSwitchSide(self): 
        if self.player.x < (Config.rows / 2):
            self.player.x = Config.areaMoveable['maxx'] - self.player.x
        else: 
            self.player.x = (Config.areaMoveable['maxx'] - self.player.x)


    def skillExplosion(self): 
        self.player.world.particleEmiter.emit(
            self.player.getLocationCenter(), 
            ParticleEffectType.explosion)


    def advance(self, dt):
        for skill, timer in self.cooldownTimers.items():
            timer.advance(dt)
