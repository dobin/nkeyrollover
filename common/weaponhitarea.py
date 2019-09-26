from typing import List

from common.coordinates import Coordinates


class WeaponHitArea(object):
    def __init__(self, hitCd=None, width=None, height=None):
        self.hitCd :List[Coordinates] = hitCd
        self.width = width
        self.height = height
