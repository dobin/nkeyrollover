import logging
import esper

from common.direction import Direction
from messaging import messaging, MessageType
from utilities.utilities import Utility
from system.graphics.renderable import Renderable
from system.gamelogic.passiveattack import PassiveAttack
from common.weaponhitarea import WeaponHitArea

logger = logging.getLogger(__name__)


class PassiveAttackProcessor(esper.Processor):
    """Implement damage-on-framechange, e.g. for puddles"""
    
    def __init__(self):
        super().__init__()


    def process(self, deltaTime):
        for _, (renderable, passiveAttack) in self.world.get_components(
                Renderable, PassiveAttack
        ):
            if renderable.texture.isFrameChanged():
                # if renderable.texture.attackFrames is not None:
                if passiveAttack.attackFrames[renderable.texture.frameIndex] is not None:
                    self.doAttack(
                        renderable,
                        passiveAttack.attackFrames[renderable.texture.frameIndex])


    def doAttack(self, renderable, damage):
        # attack
        location = renderable.getLocation()
        #hitcd = copy.deepcopy(renderable.texture.getCurrentFrame())
        frame = renderable.texture.getCurrentFrame()
        hitcd = Utility.getListFromTexture(frame)
        weaponHitArea = WeaponHitArea(hitcd, width=len(frame[0]), height=len(frame))
        direction = Direction.none
        Utility.updateCoordinateListWithBase(
            weaponHitArea=weaponHitArea, loc=location, direction=direction)
        damage = 10

        messaging.add(
            type=MessageType.AttackAt,
            data= {
                'hitLocations': hitcd,
                'damage': damage,
                'byPlayer': False,
                'direction': direction,
                'knockback': False,
                'stun': False,
                'sourceRenderable': renderable,
            }
        )
