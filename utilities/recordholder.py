import logging

from system.gamelogic.weapontype import WeaponType
from texture.character.charactertype import CharacterType

logger = logging.getLogger(__name__)


class RecordHolder(object):
    @staticmethod
    def recordAttack(weaponType :WeaponType, damage :int, name :str, characterType :CharacterType):
        l = "{} name {} attack {} damage {}".format(characterType.name, name, weaponType, damage)
        logger.record(l)

    @staticmethod
    def recordPlayerAttackCooldown(weaponType :WeaponType, time :float):
        l = "player attack {} on cooldown {}".format(weaponType, time)
        logger.record(l)