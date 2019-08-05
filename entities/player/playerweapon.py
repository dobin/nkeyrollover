import logging

from entities.characterweapon import CharacterWeapon 
from texture.phenomenatype import PhenomenaType

logger = logging.getLogger(__name__)


class PlayerWeapon(CharacterWeapon): 
   def doHit(self):
        if not self.cooldownTimer.timeIsUp():
            logging.debug("Hitting on cooldown")
            return
        self.cooldownTimer.reset() # activate cooldown

        hittedEnemies = self.parent.world.director.getEnemiesHit(self.getLocation())
        for enemy in hittedEnemies: 
            enemy.gmHandleHit( self.parent.characterStatus.getDamage() )

        self.isActive = True
        self.durationTimer.reset() # entity will setActive(false) when time is up
        self.sprite.changeTexture(PhenomenaType.hit, self.parent.direction)

