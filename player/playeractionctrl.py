
from .action import Action
from config import Config
from direction import Direction

from .baseactionctrl import BaseActionCtrl

import logging

logger = logging.getLogger(__name__)

class PlayerActionCtrl(BaseActionCtrl):
    def changeTo(self, newAction, direction):
        self.isActive = True

        if newAction is Action.walking:
            # we start, or continue, walking
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)

            # if we were already walking, dont destroy the animation state
            if self.type is not Action.walking:
                logger.info("PP Change action to1: " + str(newAction))
                self.sprite.initSprite(newAction, direction, None)
        else: 
            logger.info("PP Change action to2: " + str(newAction))
            self.duration = Config.secToFrames(1)
            self.durationLeft = Config.secToFrames(1)

            self.sprite.initSprite(newAction, direction, None)

        self.type = newAction


    def specificAdvance(self):
        # stand still after some non walking
        if self.type is Action.walking: 
            if self.durationLeft == 0:
                self.type = Action.standing
                self.sprite.initSprite(Action.standing, Direction.right, None)

        # after hitting is finished, stand still
        if self.type is Action.hitting: 
            if self.durationLeft == 0:
                self.type = Action.standing
                self.sprite.initSprite(Action.standing, Direction.right, None)

        # when dying, desintegrate
        if self.type is Action.dying: 
            if self.durationLeft == 0:
                logging.warning("PP Deactivate!")
                self.isActive = False
