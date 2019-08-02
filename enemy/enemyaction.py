
from player.action import Action
from config import Config
from player.direction import Direction

from player.baseaction import BaseAction

import logging

logger = logging.getLogger(__name__)

class EnemyAction(BaseAction):
    def changeTo(self, newAction, direction):
        self.isActive = True
        
        if newAction is Action.walking:
            # we start, or continue, walking
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)

            # if we were already walking, dont destroy the animation state
            if self.type is not Action.walking:
                logger.info("EE Change action to1: " + str(newAction))
                self.sprite.initSprite(newAction, direction)
        elif newAction is Action.dying: 
            logger.info("EE Change action to2: " + str(newAction))
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)
            self.sprite.initSprite(newAction, direction)
        else: 
            logger.info("EE Change action to3: " + str(newAction))
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)
            self.sprite.initSprite(newAction, direction)

        self.type = newAction


    def specificAdvance(self):
        # when dying, desintegrate
        if self.type is Action.dying: 
            if self.durationLeft == 0:
                logging.warning("EE Deactivate!")
                self.isActive = False