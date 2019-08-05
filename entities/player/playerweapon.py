import logging

from entities.characterweapon import CharacterWeapon 
from texture.phenomenatype import PhenomenaType

logger = logging.getLogger(__name__)


class PlayerWeapon(CharacterWeapon):
    def __init__(self, win, parentCharacter):
        super(PlayerWeapon, self).__init__(win=win, parentCharacter=parentCharacter)


    def doHit(self):
        if not self.cooldownTimer.timeIsUp():
            logging.debug("Hitting on cooldown")
            return
        self.cooldownTimer.reset() # activate cooldown

        hittedEnemies = self.parentCharacter.world.director.getEnemiesHit(self.getHitCoordinates())
        for enemy in hittedEnemies: 
            enemy.gmHandleHit( self.parentCharacter.characterStatus.getDamage() )

        self.isActive = True
        self.durationTimer.reset() # entity will setActive(false) when time is up
        self.sprite.changeTexture(PhenomenaType.hit, self.parentEntity.direction)

