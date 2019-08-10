import logging 
from entities.weapontype import WeaponType

logger = logging.getLogger(__name__)


class RecordHolder(object): 
    @staticmethod
    def recordPlayerAttack(weaponType :WeaponType, damage :int):
        l = "attack {} damage {}".format(weaponType, damage)
        logger.record(l)

    @staticmethod
    def recordPlayerAttackCooldown(weaponType :WeaponType, time :float):
        l = "attack {} on cooldown {}".format(weaponType, time)
        logger.record(l)