import logging

from entities.characterweapon import CharacterWeapon 
from texture.phenomenatype import PhenomenaType

logger = logging.getLogger(__name__)


class EnemyWeapon(CharacterWeapon):
    def __init__(self, win, parentCharacter):
        super(EnemyWeapon, self).__init__(win=win, parentCharacter=parentCharacter)


    def doHit(self):
        if not self.cooldownTimer.timeIsUp():
            return
        self.cooldownTimer.reset() # activate cooldown

        hittedPlayer = self.parentCharacter.world.director.getPlayersHit(self.getHitCoordinates())
        for player in hittedPlayer: 
            player.gmHandleHit( self.parentCharacter.characterStatus.getDamage() )

        self.isActive = True
        self.durationTimer.reset() # entity will setActive(false) when time is up
        self.sprite.changeTexture(PhenomenaType.hit, self.parentEntity.direction)
