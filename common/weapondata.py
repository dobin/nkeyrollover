from typing import Dict
from common.direction import Direction
from common.weaponhitarea import WeaponHitArea
from texture.action.actiontype import ActionType


class WeaponData(object):
    def __init__(self):
        self.actionTextureType :ActionType = None
        self.weaponHitArea :Dict[Direction, WeaponHitArea] = {}
        self.damage :int = None

        self.hitDetectionDirection = None  # not really used here anymore
