from entities.characterweapon import CharacterWeapon 
from texture.phenomenatype import PhenomenaType

class PlayerWeapon(CharacterWeapon): 
   def doHit(self):
        hittedEnemies = self.parent.world.director.getEnemiesHit(self.getLocation())
        for enemy in hittedEnemies: 
            enemy.gmHandleHit( self.parent.characterStatus.getDamage() )

        self.isActive = True
        self.durationTimer.reset()
        self.sprite.changeTexture(PhenomenaType.hit, self.parent.direction)