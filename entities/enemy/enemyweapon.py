from entities.characterweapon import CharacterWeapon 
from texture.phenomenatype import PhenomenaType

class EnemyWeapon(CharacterWeapon): 
   def doHit(self):
        hittedPlayer = self.parent.world.director.getPlayersHit(self.getLocation())
        for player in hittedPlayer: 
            player.gmHandleHit(50)

        self.isActive = True
        self.durationTimer.reset()
        self.sprite.changeTexture(PhenomenaType.hit, self.parent.direction)