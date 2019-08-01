
from player.action import Action
from config import Config
from player.direction import Direction

from player.baseaction import BaseAction

import logging

logger = logging.getLogger(__name__)

class EnemyAction(BaseAction):
    def changeTo(self, action, direction):
        self.isActive = True
        
        if action is Action.walking:
            # we start, or continue, walking
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)

            # if we were already walking, dont destroy the animation state
            if self.type is not Action.walking:
                logger.warning("EE Change action to1: " + str(action))
                self.sprite.initSprite(action, direction)
        else: 
            logger.warning("EE Change action to2: " + str(action))
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)

            self.sprite.initSprite(action, direction)

        self.type = action


    def specificAdvance(self):
        # when dying, desintegrate
        if self.type is Action.dying: 
            if self.durationLeft == 0:
                logging.warning("Deactivate!")
                self.isActive = False
