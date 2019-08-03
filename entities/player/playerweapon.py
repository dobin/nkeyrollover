from entities.characterweapon import CharacterWeapon 
from entities.action import Action

class PlayerWeapon(CharacterWeapon): 
   def doHit(self):
        hittedEnemies = self.parent.world.director.getEnemiesHit(self.getLocation())
        for enemy in hittedEnemies: 
            enemy.gmHandleHit(50)

        self.isActive = True
        self.durationTimer.reset()
        self.sprite.initSprite(Action.hit, self.parent.direction, None)