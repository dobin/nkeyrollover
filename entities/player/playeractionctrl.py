from config import Config

from entities.action import Action
from entities.direction import Direction
from entities.actionctrl import ActionCtrl
from texture.characteranimationtype import CharacterAnimationType

import logging

logger = logging.getLogger(__name__)

class PlayerActionCtrl(ActionCtrl):
    """ The Player-Character controller. Manage states, like standing->walking """

    def changeTo(self, newCharacterAnimationType, direction):
        self.parentEntity.setActive(True)

        if newCharacterAnimationType is CharacterAnimationType.walking:
            # we start, or continue, walking, endlessly
            self.durationTimer.setTimer(1.0)
            self.durationTimer.reset()

            # if we were already walking, dont destroy the animation state
            if self.action is not CharacterAnimationType.walking:
                logger.info("PP Change action to1: " + str(newCharacterAnimationType))
                self.parentEntity.sprite.changeTexture(newCharacterAnimationType, direction)
        else: 
            logger.info("PP Change action to2: " + str(newCharacterAnimationType))
            
            self.parentEntity.sprite.changeTexture(newCharacterAnimationType, direction)
            animationTime = self.parentEntity.sprite.getAnimationTime()

            self.durationTimer.setTimer(animationTime)
            self.durationTimer.reset()

        self.action = newCharacterAnimationType


    def specificAdvance(self):
        # stand still after some non walking
        if self.action is CharacterAnimationType.walking: 
            if self.durationTimer.timeIsUp():
                self.action = CharacterAnimationType.standing
                self.parentEntity.sprite.changeTexture(CharacterAnimationType.standing, Direction.right)

        # after hitting is finished, stand still
        if self.action is CharacterAnimationType.hitting: 
            if self.durationTimer.timeIsUp():
                self.action = CharacterAnimationType.standing
                self.parentEntity.sprite.changeTexture(CharacterAnimationType.standing, Direction.right)

        # when dying, desintegrate
        if self.action is CharacterAnimationType.dying: 
            if self.durationTimer.timeIsUp():
                logging.warning("PP Deactivate!")
                self.isActive = False
