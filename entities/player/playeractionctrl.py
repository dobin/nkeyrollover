from config import Config

from entities.action import Action
from entities.direction import Direction
from entities.actionctrl import ActionCtrl

import logging

logger = logging.getLogger(__name__)

class PlayerActionCtrl(ActionCtrl):
    """ The Player-Character controller. Manage states, like standing->walking """

    def changeTo(self, newAction, direction):
        self.parentEntity.setActive(True)

        if newAction is Action.walking:
            # we start, or continue, walking, endlessly
            self.durationTimer.setTimer(1.0)
            self.durationTimer.reset()

            # if we were already walking, dont destroy the animation state
            if self.action is not Action.walking:
                logger.info("PP Change action to1: " + str(newAction))
                self.parentEntity.sprite.initSprite(newAction, direction, None)
        else: 
            logger.info("PP Change action to2: " + str(newAction))
            
            self.parentEntity.sprite.initSprite(newAction, direction, None)
            animationTime = self.parentEntity.sprite.getAnimationTime()

            self.durationTimer.setTimer(animationTime)
            self.durationTimer.reset()

        self.action = newAction


    def specificAdvance(self):
        # stand still after some non walking
        if self.action is Action.walking: 
            if self.durationTimer.timeIsUp():
                self.action = Action.standing
                self.parentEntity.sprite.initSprite(Action.standing, Direction.right, None)

        # after hitting is finished, stand still
        if self.action is Action.hitting: 
            if self.durationTimer.timeIsUp():
                self.action = Action.standing
                self.parentEntity.sprite.initSprite(Action.standing, Direction.right, None)

        # when dying, desintegrate
        if self.action is Action.dying: 
            if self.durationTimer.timeIsUp():
                logging.warning("PP Deactivate!")
                self.isActive = False
