from entities.characterweapon import CharacterWeapon 
from entities.action import Action

class EnemyWeapon(CharacterWeapon): 
   def doHit(self):
        hittedPlayer = self.parent.world.director.getPlayersHit(self.getLocation())
        for player in hittedPlayer: 
            player.gmHandleHit(50)

        self.isActive = True
        self.durationTimer.reset()
        self.sprite.initSprite(Action.hit, self.parent.direction, None)